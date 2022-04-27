from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from core.admin import BaseAdmin, BaseStackedInline, BaseTabularInline
from core import utils


class EventAdmin(BaseAdmin):
    class EventApplicationInline(BaseTabularInline):
        model = EventApplication
        fields = ['resident_profile', 'status']

    model = Event
    inlines = [EventApplicationInline]
    list_display = [
        'id',
        'name',
        utils.linkify_field('campus'),
        utils.linkify_field('host'),
        'type',
        'status',
        'date',
        'created_at'
    ]
    list_filter = ['campus', 'type', 'status', 'date', 'created_at']
    search_fields = ['host__user__username', 'campus__name_ar', 'campus__name_en']


class EventApplicationAdmin(BaseAdmin):
    model = EventApplication
    list_display = [
        'id',
        utils.linkify_field('event'),
        utils.linkify_field('resident_profile'),
        'status',
        'created_at'
    ]
    list_filter = ['status', 'event', 'event__campus', 'created_at']
    search_fields = [
        'event__name',
        'event__campus__name_ar',
        'event__campus__name_en',
        'resident_profile__user__username'
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(EventApplication, EventApplicationAdmin)
