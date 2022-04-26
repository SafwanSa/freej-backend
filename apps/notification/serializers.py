from .models import *
from rest_framework import serializers
from . import queries
from apps.account.models import User


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['title', 'body']
