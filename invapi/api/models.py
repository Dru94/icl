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
    is_association_admin = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
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
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, )
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Association, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title 
    

# model to define membership
class Membership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member')
    association = models.ForeignKey(Association, on_delete=models.CASCADE, related_name='association')
    date_joined = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, default='')
    
    class Meta:
        unique_together = ['member', 'association']
    
    def __str__(self):
        return f"{self.member} - {self.association}"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from member and association names
            member_name = self.member.name.replace(" ", "-")
            association_name = self.association.title.replace(" ", "-")
            self.slug = f"{member_name}-{association_name}"
            # Check for existing slugs and add a number suffix to ensure uniqueness
            existing_slugs = Membership.objects.filter(slug__startswith=self.slug).values_list("slug", flat=True)
            if self.slug in existing_slugs:
                suffix = 2
                while f"{self.slug}-{suffix}" in existing_slugs:
                    suffix += 1
                self.slug = f"{self.slug}-{suffix}"
        super().save(*args, **kwargs)
    

class Account(TimestampedModelMixin, models.Model):
    bank_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=100)
    account_name = models.CharField(max_length=200)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, default="")
    
    def __str__(self) -> str:
        return f"{self.association.title} | {self.account_name} | {self.account_number}"
    