from rest_framework import serializers
from .models import *
from . import queries


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


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']


class PostSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    application = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = queries.get_post_reviews(post=obj)
        return ReviewSerializer(reviews, many=True).data

    def get_images(self, obj):
        images = queries.get_post_images(post=obj)
        return PostImageSerializer(images, many=True).data

    def get_application(self, obj):
        if self.context.get('show_application_status'):
            resident_profile = self.context.get('resident_profile')
            applications = queries.get_all_post_applications_by(beneficiary=resident_profile, post=obj)
            if applications.exists():
                application = applications.first()
                return {'id': application.id, 'status': application.status}
        return None


class CreatePostSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    images = serializers.ListField(child=serializers.URLField(), required=False, allow_null=True)


class UpdatePostSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    images = serializers.ListField(child=serializers.URLField(), required=False, allow_null=True)


class RateSerializer(serializers.Serializer):
    rating = serializers.IntegerField()


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
