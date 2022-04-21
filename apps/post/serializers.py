from rest_framework import serializers
from .models import *


class OwnerSerializer(serializers.ModelSerializer):
    class OwnerUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'first_name', 'last_name']

    user = OwnerUserSerializer()

    class Meta:
        model = ResidentProfile
        fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = representation['user']
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()

    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'


class CreatePostSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    # Images


class UpdatePostSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)


class RateSerializer(serializers.Serializer):
    rating = serializers.IntegerField()


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
