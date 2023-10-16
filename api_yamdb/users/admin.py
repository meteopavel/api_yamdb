from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role',)}),
)
admin.site.register(User, UserAdmin)
