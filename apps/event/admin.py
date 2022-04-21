from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
import nested_admin
from core import utils


class EventAdmin(nested_admin.NestedModelAdmin):
    class EventApplicationInline(nested_admin.NestedTabularInline):
        model = EventApplication
        extra = 0
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
    search_fields = ['host__user', 'campus']


class EventApplicationAdmin(nested_admin.NestedModelAdmin):
    model = EventApplication
    list_display = [
        'id',
        utils.linkify_field('event'),
        utils.linkify_field('resident_profile'),
        'status',
        'created_at'
    ]
    list_filter = ['status', 'event', 'event__campus', 'created_at']
    search_fields = ['event__name', 'event__campus']


admin.site.register(Event, EventAdmin)
admin.site.register(EventApplication, EventApplicationAdmin)
