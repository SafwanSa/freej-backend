from django.contrib import admin
from .models import *
from core.admin import BaseAdmin, BaseStackedInline, BaseTabularInline


@admin.register(Notification)
class NotificationAdmin(BaseAdmin):
    model = Notification
    list_display = [
        'receivers',
        'created_at',
        'title',
        'body'
    ]
    list_filter = [
        'type',
        'created_at'
    ]
    search_fields = [
        'receivers'
    ]
