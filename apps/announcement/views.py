from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from core.errors import Error, APIError
from . import queries
from apps.campus import queries as campusQueries
from apps.campus.permissions import SupervisorAccess
from .services import AnnouncementService


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


class SendAnnouncementView(APIView):
    permission_classes = [IsAuthenticated, SupervisorAccess]

    def post(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        building = resident_profile.room.building
        serializer = SendBuildingAnnouncementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        announcement = AnnouncementService.send_building_announcement(
            resident_profile=resident_profile,
            building=building,
            **serializer.validated_data
        )
        return Response(BuildingAnnouncementSerializer(announcement).data)


class DeleteAnnouncementView(APIView):
    permission_classes = [IsAuthenticated, SupervisorAccess]

    def delete(self, request, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        announcement = queries.get_building_announcement_by_id(id=pk)
        self.check_object_permissions(request=request, obj=announcement.building)
        announcement = AnnouncementService.delete_building_announcement(announcement=announcement)
        return Response(BuildingAnnouncementSerializer(announcement).data)
