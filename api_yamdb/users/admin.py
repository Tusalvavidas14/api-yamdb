from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('YaMDb', {'fields': ('bio', 'role')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('YaMDb', {'fields': ('email', 'bio', 'role')}),
    )
