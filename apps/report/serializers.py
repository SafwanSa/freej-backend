from rest_framework import serializers
from .models import *


class ReportInstanceSerializer(serializers.Serializer):
    instance_id = serializers.IntegerField()
    instance_type = serializers.CharField()
    comment = serializers.CharField(required=False, allow_null=True)


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = ['is_checked', 'checked_by']
