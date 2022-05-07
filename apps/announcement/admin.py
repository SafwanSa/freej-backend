from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from core import utils
from core.admin import BaseAdmin, BaseStackedInline, BaseTabularInline
from django_object_actions import DjangoObjectActions
from . import queries
from apps.campus import queries as campusQueries
from .services import AnnouncementService
from apps.account import queries as accountQueries


class AnnouncementAdmin(BaseAdmin):
    model = Announcement
    list_display = ['id', utils.linkify_field('sender'), 'type', 'title', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['sender__username', 'title']


class BuildingAnnouncementAdmin(DjangoObjectActions, BaseAdmin):
    model = BuildingAnnouncement
    list_display = ['id', utils.linkify_field('sender'), utils.linkify_field('building'), 'title', 'created_at']
    list_filter = ['building', 'created_at']
    search_fields = ['sender__username', 'title']
    autocomplete_fields = ['building']

    def notify_residents(modeladmin, request, instance):
        instance.save()
        building_residents = campusQueries.get_all_building_residents(building=instance.building)
        AnnouncementService.send_push_notification(
            announcement=instance,
            title=instance.title,
            body=instance.body,
            receivers=building_residents
        )

    change_actions = ('notify_residents',)


class CampusAnnouncementAdmin(DjangoObjectActions, BaseAdmin):
    model = CampusAnnouncement
    list_display = ['id', utils.linkify_field('sender'), utils.linkify_field('campus'), 'title', 'created_at']
    list_filter = ['campus', 'created_at']
    search_fields = ['sender__username', 'title']
    autocomplete_fields = ['campus']

    def render_change_form(self, request, context, *args, **kwargs):
        form = context['adminform'].form
        form.fields['sender'].queryset = accountQueries.get_staff_accounts()
        return super().render_change_form(request, context, *args, **kwargs)

    def notify_residents(modeladmin, request, instance):
        instance.save()
        campus_residents = campusQueries.get_all_campus_residents(campus=instance.campus)
        AnnouncementService.send_push_notification(
            announcement=instance,
            title=instance.title,
            body=instance.body,
            receivers=campus_residents
        )

    change_actions = ('notify_residents',)


class CommercialAnnouncementAdmin(DjangoObjectActions, BaseAdmin):
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

    def render_change_form(self, request, context, *args, **kwargs):
        form = context['adminform'].form
        form.fields['sender'].queryset = accountQueries.get_staff_accounts()
        return super().render_change_form(request, context, *args, **kwargs)

    def notify_residents(modeladmin, request, instance):
        instance.save()
        campus_residents = campusQueries.get_all_campus_residents(campus=instance.campus)
        AnnouncementService.send_push_notification(
            announcement=instance,
            title=instance.title,
            body=instance.body,
            receivers=campus_residents
        )

    change_actions = ('notify_residents',)


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(BuildingAnnouncement, BuildingAnnouncementAdmin)
admin.site.register(CampusAnnouncement, CampusAnnouncementAdmin)
admin.site.register(CommercialAnnouncement, CommercialAnnouncementAdmin)
