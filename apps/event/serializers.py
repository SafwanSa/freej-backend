from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
from . import queries


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventApplication
        fields = '__all__'


class CreateUpdateEventSerializer(serializers.Serializer):
    type = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    location_url = serializers.URLField(allow_null=True)
    date = serializers.DateTimeField()
