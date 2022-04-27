from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import *
from core.admin import BaseAdmin, BaseStackedInline, BaseTabularInline


class UserAdmin(BaseAdmin):
    model = User
    list_display = [
        'username', 'first_name', 'last_name', 'mobile_number', 'get_user_groups', 'date_joined'
    ]

    list_filter = [
        'is_superuser',
        'is_blocked',
        'date_joined',
        'last_login'
    ]

    search_fields = [
        'username', 'first_name', 'last_name', 'mobile_number'
    ]

    def get_user_groups(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append(group.name)

        return ', '.join(groups)
    get_user_groups.short_description = 'Groups'


class OTPAdmin(BaseAdmin):
    model = OTP
    list_display = ['otp', 'username', 'is_active', 'expiration_date']


class FCMTokenAdmin(BaseAdmin):
    model = FCMToken

    list_display = [
        'user',
        'is_active',
        'modified_at'
    ]

    list_filter = [
        'is_active',
        'modified_at'
    ]

    search_fields = [
        'user__username'
    ]


admin.site.register(User, UserAdmin)
admin.site.register(OTP, OTPAdmin)
admin.site.register(FCMToken, FCMTokenAdmin)
