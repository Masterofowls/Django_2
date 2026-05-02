from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin (BaseUserAdmin):
  list_display = ('username', 'full_name', 'role', 'is_active')
  list_filter = ('role', 'is_active')
  search_fields = ('username', 'fullname')
