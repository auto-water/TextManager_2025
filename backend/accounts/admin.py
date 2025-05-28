from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_frozen')
    list_filter = ('is_staff', 'is_active', 'is_frozen')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_frozen',)}), # 在 admin 中添加 is_frozen 字段
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'is_frozen',)}),
    )
    search_fields = ('username', 'email')

admin.site.register(User, UserAdmin)