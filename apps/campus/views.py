from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from core.errors import Error, APIError
from . import queries
from .permissions import ResidentProfileAccess


class ResidentProfileView(APIView):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def get(self, request):
        resident_profile = queries.get_resident_profile_by(user=request.user)
        serializer = ResidentProfileSerializer(resident_profile)
        return Response(serializer.data)


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
