from django.contrib import admin
from core.admin import BaseAdmin
from .models import *
from . import queries
from core import utils


class ReportAdmin(BaseAdmin):
    model = Report
    list_display = [
        'id',
        'instance_type',
        'get_instance',
        'created_at',
        'is_checked',
        'checked_by',
    ]
    list_filter = ['instance_type', 'created_at', 'is_checked']

    def get_instance(self, obj):
        instance = queries.get_report_instance(report=obj)
        return utils.linkify_instance(instance=instance)
    get_instance.short_description = 'Instance'


admin.site.register(Report, ReportAdmin)
