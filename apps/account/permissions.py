from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _
from .models import *


class UserAccountAccess(BasePermission):
    message = _("You don't have access to this account")

    def has_permission(self, request, view):
        user = request.user
        if user.is_blocked:
            self.message = _('User is banned!')
            return False
        return True
