from rest_framework.permissions import BasePermission
from .models import ResidentProfile
from django.utils.translation import gettext_lazy as _
from apps.account.models import GroupEnum


class ResidentProfileAccess(BasePermission):
    message = _('User has no resident profile or role.')

    def has_permission(self, request, view):
        user = request.user
        if user.is_blocked:
            self.message = _('User is banned!')
            return False
        try:
            if user.groups.filter(name=GroupEnum.Resident.value).exists() and user.resident_profile:
                return True
            return False
        except ResidentProfile.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        return False


class SupervisorAccess(BasePermission):
    message = _('User has no supervisor role or the supervisor permission is disabled.')

    def has_permission(self, request, view):
        user = request.user
        if user.is_blocked:
            self.message = _('User is banned!')
            return False
        try:
            if user.groups.filter(name=GroupEnum.Supervisor.value).exists(
            ) and user.resident_profile and user.resident_profile.is_supervisor:
                return True
            return False
        except ResidentProfile.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.resident_profile.room.building == obj:
            return True
        return False
