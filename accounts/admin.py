from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User  # your custom user model
from django.utils.translation import gettext_lazy as _


admin.site.register(User)
