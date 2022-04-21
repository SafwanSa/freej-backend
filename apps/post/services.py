from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User
from apps.campus.models import ResidentProfile, Campus


class PostService:

    @staticmethod
    def rate_post(resident_profile: ResidentProfile, post: Post, rating: int) -> Post:
        reviews = queries.get_post_reviews(post=post)
        reviews = reviews.filter(reviewer=resident_profile)
        if reviews.exists():
            raise APIError(Error.ALREADY_RATED)

        new_review = Review.objects.create(
            post=post,
            reviewer=resident_profile,
            rating=rating,
            comment=None
        )
        return new_review


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

    @staticmethod
    def apply_to_serve_request(resident_profile: ResidentProfile, post: Post) -> Application:
        """
        This is performed by the beneficiary
        """
        # Check if beneficiary already applied to the post
        application = queries.get_all_post_applications_by(post=post, beneficiary=resident_profile).first()
        if application:
            raise APIError(Error.ALREADY_APPLIED)

        # check if the beneficiary is the same as the owner
        if post.owner == resident_profile:
            raise APIError(Error.OWNER_CANNOT_APPLY)

        application = Application.objects.create(
            post=post,
            beneficiary=resident_profile,
            status=Application.ApplicationStatus.Pending.value,
            description='A resident has applied to your request of service'
        )
        return application

    @staticmethod
    def cancel_serve_request_application(resident_profile: ResidentProfile, post: Post) -> Application:
        """
        This is performed by the beneficiary
        """
        application = queries.get_all_post_applications_by(post=post, beneficiary=resident_profile).first()

        if application.status != Application.ApplicationStatus.Pending.value:
            raise APIError(Error.CANNOT_CANCEL)

        application.status = Application.ApplicationStatus.Cancelled.value
        return application

    @staticmethod
    def accept_serve_request_application(resident_profile: ResidentProfile, application: Application) -> Application:
        """
        This is performed by the owner
        """
        # check if the resident is the owner
        if application.post.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        # Accpet the application
        application.status = Application.ApplicationStatus.Accepted.value
        application.save()

        # Reject all other applications
        post = application.post
        all_applications = queries.get_all_post_applications_by(post=post, beneficiary=None, status=None)
        other_applications = all_applications.exclude(id=application.id)
        for app in other_applications:
            app.status = Application.ApplicationStatus.Rejected.value
        return application

    @staticmethod
    def reject_serve_request_application(resident_profile: ResidentProfile, application: Application) -> Application:
        """
        This is performed by the owner
        """
        # check if the resident is the owner
        if application.post.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        # Accpet the application
        application.status = Application.ApplicationStatus.Rejected.value
        application.save()

        return application
