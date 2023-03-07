from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from django.utils.text import slugify
from .managers import CustomUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Create your models here.
class TimestampedModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Member(AbstractBaseUser, PermissionsMixin, TimestampedModelMixin):
    email = models.EmailField(_("email_address"), unique=True)
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=13)
    national_id = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='media/', null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    associations = models.ManyToManyField('Association', related_name='member_association')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='member_permissions',
        help_text=_('The permissions this member has.'),
    )
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='member_groups',
        help_text='The groups this member belongs to. A member will get all permissions granted to each of their groups.'
    )
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact', 'national_id']
    
    def clean(self):
        # check the number of associations
        count = self.associations.count()
        if count < 1 or count > 3:
            raise ValidationError('A member can only belong to one, two, or three associations.')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Member, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} | {self.email}"
    

class Association(TimestampedModelMixin, models.Model):
    title = models.CharField(max_length=200,)
    tin_number = models.CharField(max_length=200,)
    constitution = models.FileField(upload_to='constitutions/')
    contact = models.CharField(max_length=13)
    email = models.EmailField(unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Association, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title 
    

# model to define membership
class Membership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['member', 'association']
    
    def __str__(self):
        return f"{self.member} - {self.association}"
    
    