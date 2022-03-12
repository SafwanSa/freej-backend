from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import *

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


class OTPAdmin(admin.ModelAdmin):
    model = OTP
    list_display = ['otp', 'username', 'is_active', 'expiration_date']


admin.site.register(OTP, OTPAdmin)
