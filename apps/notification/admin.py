from django.contrib import admin
from .models import *
from core.admin import BaseAdmin, BaseStackedInline, BaseTabularInline


@admin.register(Notification)
class NotificationAdmin(BaseAdmin):
    model = Notification
    list_display = [
        'id',
        'get_receivers',
        'title',
        'body',
        'created_at'
    ]
    list_filter = [
        'type',
        'created_at'
    ]
    search_fields = [
        'receivers'
    ]

    def get_receivers(self, obj):
        receivers = obj.receivers.split(',')
        if len(receivers) > 1:
            return str(len(receivers)) + ' receivers'
        else:
            return receivers
    get_receivers.short_description = 'Receivers'
