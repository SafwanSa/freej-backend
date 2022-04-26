from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from . import queries
from apps.campus import queries as campusQueries
from apps.campus.permissions import ResidentProfileAccess


class NotificationView(APIView):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def get(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        notifications = queries.get_push_notifications_by(resident_profile=resident_profile)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
