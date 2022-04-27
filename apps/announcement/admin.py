from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from core import utils
from core.admin import BaseAdmin, BaseStackedInline, BaseTabularInline


class AnnouncementAdmin(BaseAdmin):
    model = Announcement
    list_display = ['id', utils.linkify_field('sender'), 'type', 'title', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['sender__username', 'title']


class BuildingAnnouncementAdmin(BaseAdmin):
    model = BuildingAnnouncement
    list_display = ['id', utils.linkify_field('sender'), utils.linkify_field('building'), 'title', 'created_at']
    list_filter = ['building', 'created_at']
    search_fields = ['sender__username', 'title']


class CampusAnnouncementAdmin(BaseAdmin):
    model = CampusAnnouncement
    list_display = ['id', utils.linkify_field('sender'), utils.linkify_field('campus'), 'title', 'created_at']
    list_filter = ['campus', 'created_at']
    search_fields = ['sender__username', 'title']


class CommercialAnnouncementAdmin(BaseAdmin):
    model = CommercialAnnouncement
    list_display = [
        'id',
        utils.linkify_field('sender'),
        utils.linkify_field('campus'),
        'advertiser_name',
        'impressions',
        'title',
        'created_at'
    ]
    list_filter = ['campus', 'created_at']
    search_fields = ['sender__username', 'title']


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(BuildingAnnouncement, BuildingAnnouncementAdmin)
admin.site.register(CampusAnnouncement, CampusAnnouncementAdmin)
admin.site.register(CommercialAnnouncement, CommercialAnnouncementAdmin)
