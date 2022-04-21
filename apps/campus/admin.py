from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
import nested_admin
from core import utils


class CampusAdmin(nested_admin.NestedModelAdmin):
    class BuildingInline(nested_admin.NestedTabularInline):
        model = Building
        extra = 0
        fields = ['name', 'supervisor', 'whatsApp_link']

    model = Campus
    inlines = [BuildingInline]
    list_display = ['id', 'name_en', 'name_ar', 'email_domain', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name_en', 'name_ar']


class BuildingAdmin(nested_admin.NestedModelAdmin):
    class RoomInline(nested_admin.NestedTabularInline):
        model = Room
        extra = 0
        fields = ['name']

    model = Building
    inlines = [RoomInline]
    list_display = ['id', 'name', utils.linkify_field('campus'), utils.linkify_field('supervisor'), 'created_at']
    list_filter = ['campus', 'created_at']
    search_fields = ['name', 'supervisor__user__username']


class RoomAdmin(nested_admin.NestedModelAdmin):
    class ResidentInline(nested_admin.NestedTabularInline):
        model = ResidentProfile
        extra = 0
        fields = ['user', 'is_supervisor']

    model = Building
    inlines = [ResidentInline]
    list_display = ['id', 'name', utils.linkify_field('building'), 'created_at']
    list_filter = ['building__campus', 'created_at']
    search_fields = ['name']


class MaintenanceIssueAdmin(nested_admin.NestedModelAdmin):
    model = MaintenanceIssue
    list_display = [
        'id',
        utils.linkify_field('building'),
        utils.linkify_field('reported_by'),
        'type',
        'reported_fixed',
        'status',
        'created_at'
    ]
    list_filter = ['building__campus', 'created_at']
    search_fields = ['building__name', 'building__campus__name_en', 'building__campus__name_ar']


class ResidentProfileAdmin(nested_admin.NestedModelAdmin):
    model = ResidentProfile
    list_display = [
        'id',
        utils.linkify_field('user'),
        'get_building',
        utils.linkify_field('room'),
        'is_supervisor',
        'created_at'
    ]
    list_filter = ['room__building__campus', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__mobile_number']

    def get_building(self, obj):
        return utils.linkify_instance(obj.room.building)
    get_building.short_description = 'Building'


admin.site.register(Campus, CampusAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(MaintenanceIssue, MaintenanceIssueAdmin)
admin.site.register(ResidentProfile, ResidentProfileAdmin)
