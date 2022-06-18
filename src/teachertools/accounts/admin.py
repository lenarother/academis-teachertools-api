from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import User

admin.site.register(User, AuthUserAdmin)
