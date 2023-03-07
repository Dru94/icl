from django.contrib import admin
from .models import Member, Association, Membership, Account


# Register your models here.
admin.site.register(Member)
admin.site.register(Association)
admin.site.register(Membership)
admin.site.register(Account)