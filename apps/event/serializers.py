from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
from . import queries
from apps.account.models import User


class HostSerializer(serializers.ModelSerializer):
    class HostUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['first_name', 'last_name']

    user = HostUserSerializer()

    class Meta:
        model = ResidentProfile
        fields = ['id', 'user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key, value in representation.pop('user').items():
            representation[key] = value
        # representation = representation['user']
        return representation


class EventJoinerSerializer(serializers.ModelSerializer):
    class EventJoinerUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['first_name', 'last_name', 'mobile_number']

    user = EventJoinerUserSerializer()

    class Meta:
        model = ResidentProfile
        fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # for key, value in representation.pop('user').items():
        #     representation[key] = value
        representation = representation['user']
        return representation


class EventApplicationSerializer(serializers.ModelSerializer):

    resident_profile = EventJoinerSerializer()

    class Meta:
        model = EventApplication
        fields = '__all__'


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['image']


class EventSerializer(serializers.ModelSerializer):

    application_status = serializers.SerializerMethodField()
    host = HostSerializer()
    applications = EventApplicationSerializer(many=True)
    images = EventImageSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        images = representation.pop('images')
        representation['images'] = []
        for image in images:
            representation['images'].append(image.get(('image')))
        return representation

    def get_application_status(self, obj):
        if self.context.get('show_application_status'):
            resident_profile = self.context.get('resident_profile')
            applications = queries.get_events_applications_by(resident_profile=resident_profile, event=obj)
            if applications.exists():
                application = applications.first()
                return application.status
        return None


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
    images = serializers.ListField(child=serializers.URLField(), required=False, allow_null=True)
