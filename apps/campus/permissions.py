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
