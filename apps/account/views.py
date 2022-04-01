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
from apps.campus.serializers import ResidentProfileSerializer


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
        resident_profile = ResidentService.create_resident_profile(**serializer.data)
        return Response(ResidentProfileSerializer(resident_profile).data)


class ResidentTokenObtainPairView(TokenObtainPairView):
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ResidentTokenRefreshView(TokenRefreshView):
    def post(self, request):
        return super().post(request)

# ------------------------------- Forget Password Views -------------------------------


class RequestOTPView(APIView):

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = AuthService.request_change_password_otp(**serializer.data)
        return Response({
            'message': _('OTP is sent. You can request a new one after {} seconds').format(Conf.OTP_WAITING_PERIOD()),
            'waiting_seconds': Conf.OTP_WAITING_PERIOD()
        })


class CheckOTPView(APIView):

    def post(self, request):
        serializer = CheckOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = AuthService.check_otp(**serializer.data)
        return Response({'message': _('OTP is valid')})


class ChangePasswordView(APIView):

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.change_password(**serializer.data)
        return Response({'message': _('Password changed successfully')})
