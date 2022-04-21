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
        rqst = queries.get_campus_post_by_id(campus=campus, id=pk)
        serializer = PostSerializer(rqst)
        return Response(serializer.data)

    def create(self, request):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rqst = RequestService.create_request(resident_profile=resident_profile, **serializer.validated_data)
        return Response(PostSerializer(rqst).data)

    def partial_update(self, request, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        rqst = queries.get_campus_post_by_id(campus=resident_profile.room.building.campus, id=pk)
        serializer = UpdatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rqst = RequestService.update_request(
            resident_profile=resident_profile,
            request=rqst,
            **serializer.validated_data
        )
        return Response(PostSerializer(rqst).data)

    def destroy(self, request, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        rqst = queries.get_campus_post_by_id(campus=resident_profile.room.building.campus, id=pk)
        rqst = RequestService.delete_request(resident_profile=resident_profile, request=rqst)
        return Response(PostSerializer(rqst).data)


class ReviewView(APIView):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def post(self, request, post_id):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        campus = resident_profile.room.building.campus
        post = queries.get_campus_post_by_id(campus=campus, id=post_id)
        serializer = RateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = PostService.rate_post(resident_profile=resident_profile, post=post, **serializer.validated_data)
        return Response(ReviewSerializer(review).data)


class RequestApplicationsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ResidentProfileAccess]

    def create(self, request, post_id):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        campus = resident_profile.room.building.campus
        post = queries.get_campus_post_by_id(campus=campus, id=post_id)
        application = RequestService.apply_to_serve_request(resident_profile=resident_profile, post=post)
        return Response(ApplicationSerializer(application).data)

    def partial_update(self, request, post_id, pk):
        resident_profile = campusQueries.get_resident_profile_by(user=request.user)
        application = queries.get_application_by_id(id=pk)
        action = request.GET.get('action', None)
        application = RequestService.update_application(
            resident_profile=resident_profile,
            application=application,
            action=action
        )
        return Response(ApplicationSerializer(application).data)
