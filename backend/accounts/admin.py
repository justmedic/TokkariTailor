from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'phone', 'is_active', 'is_staff')
    
    list_filter = ('is_active', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
    )
 
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'phone')
    # Критерий сортировки списка пользователей (по умолчанию по email)
    ordering = ('email',)
