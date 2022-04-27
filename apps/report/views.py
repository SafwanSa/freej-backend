from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.errors import Error, APIError
from . import queries
from apps.campus.permissions import SupervisorAccess, ResidentProfileAccess
from .services import ReportService
from apps.campus import queries as campusQueries


class ReportView(APIView):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def post(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        serializer = ReportInstanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = ReportService.report_instance(resident_profile=resident_profile, **serializer.validated_data)
        return Response(ReportSerializer(report).data)
