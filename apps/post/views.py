from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from core.errors import Error, APIError
from . import queries
from apps.campus import queries as campusQueries
from apps.campus.permissions import SupervisorAccess, ResidentProfileAccess
from .services import OfferService, RequestService, PostService


class OfferViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def list(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        campus = resident_profile.room.building.campus
        offers = queries.get_all_campus_offers(campus=campus)
        serializer = PostSerializer(offers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        campus = resident_profile.room.building.campus
        offer = queries.get_campus_post_by_id(campus=campus, id=pk)
        serializer = PostSerializer(offer)
        return Response(serializer.data)

    def create(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offer = OfferService.create_offer(resident_profile=resident_profile, **serializer.validated_data)
        return Response(PostSerializer(offer).data)

    def partial_update(self, request, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        offer = queries.get_campus_post_by_id(campus=resident_profile.room.building.campus, id=pk)
        serializer = UpdatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offer = OfferService.update_offer(resident_profile=resident_profile, offer=offer, **serializer.validated_data)
        return Response(PostSerializer(offer).data)

    def destroy(self, request, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        offer = queries.get_campus_post_by_id(campus=resident_profile.room.building.campus, id=pk)
        offer = OfferService.delete_offer(resident_profile=resident_profile, offer=offer)
        return Response(PostSerializer(offer).data)


class RequestViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def list(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        campus = resident_profile.room.building.campus
        requests = queries.get_all_campus_requests(campus=campus)
        serializer = PostSerializer(requests, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        campus = resident_profile.room.building.campus
        request = queries.get_campus_post_by_id(campus=campus, id=pk)
        serializer = PostSerializer(request)
        return Response(serializer.data)

    def create(self, request):
        pass

    def partial_update(self, request, pk):
        pass

    def destroy(self, request, pk):
        pass
