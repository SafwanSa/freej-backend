from rest_framework import serializers
from .models import *


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    class RoomSerializer(serializers.ModelSerializer):
        class Meta:
            model = Room
            fields = '__all__'

    rooms = RoomSerializer(many=True)

    class Meta:
        model = Building
        fields = '__all__'
