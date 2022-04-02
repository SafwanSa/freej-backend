from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from core.errors import Error, APIError
from . import queries
from apps.campus import queries as campusQueries
from apps.campus.permissions import SupervisorAccess, ResidentProfileAccess
from rest_framework import viewsets
from .services import EventService


class EventViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def list(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        campus = resident_profile.room.building.campus
        events = queries.get_all_campus_events(campus=campus)
        serializer = EventSerializer(
            events,
            many=True,
            context={
                'show_application_status': True,
                'resident_profile': resident_profile})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        event = queries.get_event_by_id(id=pk)
        serializer = EventSerializer(
            event,
            context={
                'show_application_status': True,
                'resident_profile': resident_profile})
        return Response(serializer.data)

    def create(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        serializer = CreateUpdateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = EventService.create_event(resident_profile=resident_profile, **serializer.validated_data)
        return Response(EventSerializer(event).data)

    def partial_update(self, request, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        event = queries.get_event_by_id(id=pk)
        serializer = CreateUpdateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = EventService.update_event(resident_profile=resident_profile, event=event, **serializer.validated_data)
        return Response(EventSerializer(event).data)

    def destroy(self, request, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        event = queries.get_event_by_id(id=pk)
        event = EventService.delete_event(resident_profile=resident_profile, event=event)
        serializer = EventSerializer(event)
        return Response(serializer.data)


class EventApplicationView(APIView):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def post(self, request, event_id):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        event = queries.get_event_by_id(id=event_id)
        application = EventService.join_event(resident_profile=resident_profile, event=event)
        serializer = EventApplicationSerializer(application)
        return Response(serializer.data)

    def delete(self, request, event_id):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        event = queries.get_event_by_id(id=event_id)
        application = EventService.leave_event(resident_profile=resident_profile, event=event)
        serializer = EventApplicationSerializer(application)
        return Response(serializer.data)
