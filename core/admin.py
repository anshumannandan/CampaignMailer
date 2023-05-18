from django.contrib import admin
from .models import User, Campaign
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    ordering = ['first_name', 'is_active']
    list_display = ['id', 'first_name', 'email', 'is_active']
    list_filter = ('is_active','is_superuser')
    filter_horizontal = ()
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff','is_active')}),
    )
    add_fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff','is_active')}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Campaign)