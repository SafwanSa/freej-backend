from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
from . import queries
from core.validators import _PHONE_REGEX
from .services import BuildingService


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
        class SupervisorSerializer(serializers.ModelSerializer):
            class SupervisorUserSerializer(serializers.ModelSerializer):
                class Meta:
                    model = User
                    fields = ['first_name', 'last_name', 'mobile_number']
            user = SupervisorUserSerializer()

            class Meta:
                model = ResidentProfile
                fields = ['id', 'user']

            def to_representation(self, instance):
                representation = super().to_representation(instance)
                for key, value in representation.pop('user').items():
                    representation[key] = value
                # representation = representation['user']
                return representation

        supervisor = SupervisorSerializer()
        statistics = serializers.SerializerMethodField()

        class Meta:
            model = Building
            exclude = ['campus']

        def get_statistics(self, obj):
            data = {
                'num_of_residents': BuildingService.get_num_building_residents(building=obj, with_blocked=False),
                'num_of_blocked_residents': BuildingService.get_num_building_residents(building=obj, with_blocked=True),
                'num_of_posts': BuildingService.get_num_of_posts_by_building(building=obj),
                'num_of_issues': BuildingService.get_num_of_building_issues(building=obj),
                'num_of_events': BuildingService.get_num_of_building_events(building=obj),
                'num_of_building_announcements': BuildingService.get_num_of_building_announcements(building=obj),
                'num_of_transactions': BuildingService.get_num_of_building_applications(building=obj),
            }
            return data

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


class EditProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_null=True)
    last_name = serializers.CharField(allow_null=True)
    mobile_number = serializers.RegexField(_PHONE_REGEX.regex, allow_null=True)
    photo = serializers.URLField(required=False, allow_null=True)
    room_id = serializers.IntegerField(required=False, allow_null=True)


class EditBuildingProfileSerializer(serializers.Serializer):
    location_url = serializers.URLField(required=False, allow_null=True)
    whatsApp_link = serializers.URLField(required=False, allow_null=True)


class MaintenanceIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceIssue
        fields = '__all__'


class ReportMaintenanceIssueSerializer(serializers.Serializer):
    type = serializers.CharField()
    description = serializers.CharField()
