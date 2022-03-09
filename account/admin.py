from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_superuser')
    searche_fields = ('email', 'username', 'is_admin', 'is_staff')
    readonly_fields = ('date_joined', 'last_login')

admin.site.register(Account, AccountAdmin)