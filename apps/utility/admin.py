from django.contrib import admin
from .models import *
from .admin_forms import ConfigAdminForm
from apps.account.models import GroupEnum


class ConfigAdmin(admin.ModelAdmin):
    form = ConfigAdminForm

    def get_form(self, request, obj=None, **kwargs):

        AdminForm = super().get_form(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                kwargs['config'] = obj
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest

    def get_readonly_fields(self, request, obj=None):
        if obj:
            is_allowed = request.user.groups.filter(
                name=GroupEnum.Admin.value).exists()
            if is_allowed:
                return []
            else:
                return ['is_system', 'is_private']
        else:
            return []

    list_display = [
        'key',
        'value',
        'tag',
        'description',
        'is_private',
        'is_system'
    ]

    list_filter = [
        'tag',
        'is_system',
        'is_private'
    ]


admin.site.register(Config, ConfigAdmin)
