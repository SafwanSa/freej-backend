from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.campus.services import ResidentService
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.utils.translation import gettext_lazy as _
from core.errors import Error, APIError
from rest_framework.pagination import PageNumberPagination
from .services import *


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = AccountService.register_resident(**serializer.data)
        return Response({
            'message': _('OTP is sent. You can request a new one after {} seconds').format(Conf.OTP_WAITING_PERIOD()),
            'waiting_seconds': Conf.OTP_WAITING_PERIOD()
        })


class ConfirmRegisterView(APIView):

    def post(self, request):
        serializer = ConfirmRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = ResidentService.create_resident_profile(**serializer.data)
        return Response(UserSerializer(user).data)


class ResidentTokenObtainPairView(TokenObtainPairView):
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ResidentTokenRefreshView(TokenRefreshView):
    def post(self, request):
        return super().post(request)
