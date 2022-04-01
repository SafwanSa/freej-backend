from rest_framework import serializers
from .models import *


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class CampusAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusAnnouncement
        fields = '__all__'


class BuildingAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingAnnouncement
        fields = '__all__'


class CommercialAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialAnnouncement
        exclude = ['impressions']


class SendBuildingAnnouncementSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
