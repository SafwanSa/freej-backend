from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
from . import queries


class EventSerializer(serializers.ModelSerializer):

    application_status = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

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
