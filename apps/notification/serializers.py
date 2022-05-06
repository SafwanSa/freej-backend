from .models import *
from rest_framework import serializers
from . import queries
from apps.account.models import User
import json


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        exclude = ['receivers', 'type', 'template', 'result']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        data = representation.pop('data')
        try:
            if data:
                data.replace("'", '"')
                data = json.loads(data)
                type = data.get('type')
                instance_id = data.get('instance_id')
                representation['type'] = type
                representation['instance_id'] = instance_id
            else:
                representation['type'] = None
                representation['instance_id'] = None
        except Exception:
            representation['type'] = None
            representation['instance_id'] = None
        return representation
