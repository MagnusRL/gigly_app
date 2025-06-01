from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Task, Application, SavedTaskTemplate
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import reverse

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'name', 'is_buyer',]
    #list_display = ['email', 'name', 'is_buyer', 'is_seller', 'is_staff', 'is_superuser']
    search_fields = ['email', 'name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'bio', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_buyer', 'is_seller', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_buyer', 'is_seller', 'is_staff', 'is_superuser'),
        }),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'buyer', 'price', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'buyer__email')

admin.site.register(User, UserAdmin)
admin.site.register(Application)
admin.site.register(SavedTaskTemplate)
