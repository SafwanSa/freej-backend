from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User
from apps.campus.models import ResidentProfile, Campus


class PostService:

    @staticmethod
    def create_post():
        pass


class OfferService(PostService):

    @staticmethod
    def create_offer(resident_profile: ResidentProfile, title: str, description: str) -> Post:
        campus = resident_profile.room.building.campus
        new_offer = Post.objects.create(
            type=Post.PostType.Offer.value,
            campus=campus,
            owner=resident_profile,
            title=title,
            description=description,
        )
        return new_offer

    @staticmethod
    def update_offer(resident_profile: ResidentProfile, offer: Post, is_active: bool = None,
                     title: str = None, description: str = None) -> Post:
        if offer.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        if offer:
            offer.title = title
        if description:
            offer.description = description
        if is_active is not None:
            offer.is_active = is_active
        offer.save()
        return offer

    @staticmethod
    def delete_offer(resident_profile: ResidentProfile, offer: Post) -> Post:
        if offer.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        offer.is_deleted = True
        offer.save()
        return offer


class RequestService(PostService):

    @staticmethod
    def create_request(resident_profile: ResidentProfile, title: str, description: str) -> Post:
        campus = resident_profile.room.building.campus
        new_request = Post.objects.create(
            type=Post.PostType.Request.value,
            campus=campus,
            owner=resident_profile,
            title=title,
            description=description,
        )
        return new_request

    @staticmethod
    def update_request(resident_profile: ResidentProfile, request: Post, is_active: bool = None,
                       title: str = None, description: str = None) -> Post:
        if request.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        if request:
            request.title = title
        if description:
            request.description = description
        if is_active is not None:
            request.is_active = is_active
        request.save()
        return request

    @staticmethod
    def delete_request(resident_profile: ResidentProfile, request: Post) -> Post:
        if request.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        request.is_deleted = True
        request.save()
        return request
