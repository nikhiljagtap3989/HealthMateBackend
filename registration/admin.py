from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.models import User

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.admin import UserAdmin



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserAdminForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')

