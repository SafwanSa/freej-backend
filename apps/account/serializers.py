from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .services import AuthService


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
    pass
