from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from core.errors import Error, APIError
from . import queries
from .permissions import ResidentProfileAccess
from .services import ResidentService, BuildingService


class ResidentProfileView(APIView):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def get(self, request):
        resident_profile = queries.get_resident_profile_by(user=request.user)
        serializer = ResidentProfileSerializer(resident_profile)
        return Response(serializer.data)

    def patch(self, request):
        resident_profile = queries.get_resident_profile_by(user=request.user)
        serializer = EditProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resident_profile = ResidentService.edit_profile(resident_profile=resident_profile, **serializer.validated_data)
        return Response(ResidentProfileSerializer(resident_profile).data)


class BuildingIssuesView(APIView):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def get(self, request):
        resident_profile = queries.get_resident_profile_by(user=request.user)
        building = resident_profile.room.building
        issues = queries.get_building_issues(building=building)
        serializer = MaintenanceIssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request):
        resident_profile = queries.get_resident_profile_by(user=request.user)
        building = resident_profile.room.building
        serializer = ReportMaintenanceIssueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        issue = BuildingService.report_issue(
            resident_profile=resident_profile,
            building=building,
            **serializer.validated_data)
        return Response(MaintenanceIssueSerializer(issue).data)


class FixBuildingIssuesView(APIView):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def post(self, request, pk):
        resident_profile = queries.get_resident_profile_by(user=request.user)
        issue = queries.get_issue_by_id(id=pk)
        issue = BuildingService.report_issue_with_fix(issue=issue, resident_profile=resident_profile)
        return Response(MaintenanceIssueSerializer(issue).data)

# ------------------------------------------ # Signup views # ------------------------------------------


class CampusesView(APIView):

    def get(self, request):
        campuses = queries.get_all_campuses()
        serializer = CampusSerializer(campuses, many=True)
        return Response(serializer.data)


class BuildingsView(APIView):

    def get(self, request, campus_id):
        campus = queries.get_campus_by_id(id=campus_id)
        buildings = queries.get_campus_buildings(campus=campus)
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)
