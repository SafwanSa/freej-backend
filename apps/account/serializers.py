from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .services import AuthService
from core.validators import _STUDENT_ID_REGEX


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
    username = serializers.RegexField(regex=_STUDENT_ID_REGEX.regex)
    password = serializers.CharField()


class ConfirmRegisterSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    username = serializers.RegexField(regex=_STUDENT_ID_REGEX.regex)
    password = serializers.CharField()
    otp = serializers.CharField(max_length=4)
