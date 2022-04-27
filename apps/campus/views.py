from apps.event.serializers import EventSerializer
from apps.post.serializers import PostSerializer
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from core.errors import Error, APIError
from . import queries
from .permissions import ResidentProfileAccess, SupervisorAccess
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


class EditBuildingView(APIView):
    permission_classes = [IsAuthenticated, SupervisorAccess]

    def patch(self, request):
        resident_profile = queries.get_resident_profile_by(user=request.user)
        building = resident_profile.room.building
        self.check_object_permissions(request=request, obj=building)
        serializer = EditBuildingProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        building = BuildingService.update_building(building=building, **serializer.validated_data)
        return Response(BuildingSerializer(building).data)
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

# ------------------------------------------ # Resident specific data views # ------------------------------------------


class ResidentPostsView(APIView):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]
    description = 'All the posts the user applied to or created'

    def get(self, request):
        resident_profile = queries.get_resident_profile_by(user=request.user)
        posts = queries.get_resident_posts_by(resident_profile=resident_profile)
        serializer = PostSerializer(posts, many=True, context={
            'show_application_status': True,
            'resident_profile': resident_profile
        })
        return Response(serializer.data)


class ResidentEventsView(APIView):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]
    description = 'All the events that the resident is joined/hosted'

    def get(self, request):
        resident_profile = queries.get_resident_profile_by(user=request.user)
        events = queries.get_resident_events_by(resident_profile=resident_profile)
        serializer = EventSerializer(events, many=True, context={
            'show_application_status': True,
            'resident_profile': resident_profile
        })
        return Response(serializer.data)
