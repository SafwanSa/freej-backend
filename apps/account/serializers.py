from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .services import AuthService
from core import validators


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token = AuthService.optain_access_token(
            group=GroupEnum.Resident,
            user=user,
            token=token
        )
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class RegisterSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    email = serializers.EmailField()
    password = serializers.CharField()


class ConfirmRegisterSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    email = serializers.EmailField()
    password = serializers.CharField()
    otp = serializers.CharField(max_length=4)


# ------------------------------- Forget Password Serializers -------------------------------

class RequestOTPSerializer(serializers.Serializer):
    username = serializers.EmailField()


class CheckOTPSerializer(serializers.Serializer):
    username = serializers.EmailField()
    otp = serializers.CharField(max_length=4)


class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.EmailField()
    new_password = serializers.CharField()
