from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from core.errors import Error, APIError
from . import queries
from apps.campus import queries as campusQueries


class CampusAndBuildingAnnouncementsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        building = resident_profile.room.building
        building_announcements = queries.get_building_announcements(building=building)
        campus_announcements = queries.get_campus_announcements(campus=building.campus)
        serializer = AnnouncementSerializer(building_announcements.union(campus_announcements), many=True)
        return Response(serializer.data)


class CommercialAnnouncementsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        campus = resident_profile.room.building.campus
        commercial_announcements = queries.get_campus_commercial_announcements(campus=campus)
        serializer = CommercialAnnouncementSerializer(commercial_announcements, many=True)
        return Response(serializer.data)
