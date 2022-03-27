from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
from . import queries


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


class ResidentProfileSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class GroupSerializer(serializers.ModelSerializer):
            class Meta:
                model = Group
                fields = '__all__'
        groups = GroupSerializer(many=True)

        class Meta:
            model = User
            fields = ['username', 'mobile_number', 'first_name', 'last_name', 'groups', 'lang']

    class CampusSerializer(serializers.ModelSerializer):
        class Meta:
            model = Campus
            fields = '__all__'

    class RoomSerializer(serializers.ModelSerializer):
        class Meta:
            model = Room
            exclude = ['building']

    class BuildingSerializer(serializers.ModelSerializer):
        class Meta:
            model = Building
            exclude = ['supervisor', 'campus']

    user = UserSerializer()
    campus_details = serializers.SerializerMethodField()

    class Meta:
        model = ResidentProfile
        fields = '__all__'

    def get_campus_details(self, obj):
        building = obj.room.building
        campus = building.campus

        building_sr = self.BuildingSerializer(building).data
        building_sr['room'] = self.RoomSerializer(obj.room).data
        campus_sr = self.CampusSerializer(campus).data
        campus_sr['building'] = building_sr

        return campus_sr

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['account'] = representation.pop('user')
        return representation
