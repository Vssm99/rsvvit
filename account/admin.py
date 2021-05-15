from django.contrib import admin
from .models import BlogUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.


admin.site.register(BlogUser, UserAdmin)
UserAdmin.fieldsets += (
    "Custom Detail:", {'fields': (
        'mobile_no', 'en_no',  'year', 'sem', 'gender', 'profile_image',), }
),
