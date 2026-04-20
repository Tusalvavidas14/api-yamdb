from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('YaMDb', {'fields': ('bio', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('YaMDb', {'fields': ('email', 'bio', 'role')}),
    )
