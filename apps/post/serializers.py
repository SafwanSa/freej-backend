from rest_framework import serializers
from .models import *
from . import queries


class OwnerSerializer(serializers.ModelSerializer):
    class OwnerUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['first_name', 'last_name', 'mobile_number']

    user = OwnerUserSerializer()

    class Meta:
        model = ResidentProfile
        fields = ['id', 'user', 'num_of_raters', 'rating']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key, value in representation.pop('user').items():
            representation[key] = value
        # representation = representation['user']
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']


class BeneficiarySerializer(serializers.ModelSerializer):
    class BeneficiaryUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['first_name', 'last_name', 'mobile_number']

    user = BeneficiaryUserSerializer()

    class Meta:
        model = ResidentProfile
        fields = ['id', 'user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key, value in representation.pop('user').items():
            representation[key] = value
        # representation = representation['user']
        return representation


class ApplicationSerializer(serializers.ModelSerializer):

    beneficiary = BeneficiarySerializer()

    class Meta:
        model = Application
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    application_status = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)
    images = PostImageSerializer(many=True)
    applications = ApplicationSerializer(many=True)

    class Meta:
        model = Post
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
            applications = queries.get_all_post_applications_by(beneficiary=resident_profile, post=obj)
            if applications.exists():
                application = applications.first()
                return application.status
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
    comment = serializers.CharField(required=False, allow_null=True)
