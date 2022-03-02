from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.utils.translation import gettext_lazy as _
from core.errors import Error, APIError
from rest_framework.pagination import PageNumberPagination


class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    description = "This endpoint return the list of users"


class ExampleErrorView(APIView):

    def get(self, request):
        raise APIError(Error._DEFAULT_MESSAGE, extra=['This is a default error message. Wehoo!'])
        return Response({})


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request):
        return super().post(request)
