from django.contrib import admin
from .models import *


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
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
