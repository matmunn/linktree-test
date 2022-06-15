"""Admin configuration for auth demo."""


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth_demo.models import User

admin.site.register(User, UserAdmin)
