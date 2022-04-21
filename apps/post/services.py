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

    @staticmethod
    def create_post(type: Post.PostType, resident_profile: ResidentProfile, title: str, description: str) -> Post:
        campus = resident_profile.room.building.campus
        new_post = Post.objects.create(
            type=type.value,
            campus=campus,
            owner=resident_profile,
            title=title,
            description=description,
        )
        return new_post

    @staticmethod
    def update_post(resident_profile: ResidentProfile, post: Post, is_active: bool = None,
                    title: str = None, description: str = None) -> Post:

        if post.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        if post:
            post.title = title
        if description:
            post.description = description
        if is_active is not None:
            post.is_active = is_active
        post.save()
        return post

    @staticmethod
    def delete_post(resident_profile: ResidentProfile, post: Post) -> Post:
        if post.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        post.is_deleted = True
        post.save()

        # TODO: Reject/delete all its applications
        return post

    @staticmethod
    def apply_to_post(type: str, resident_profile: ResidentProfile, post: Post) -> Application:
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

        description = 'A resident has applied to your request of service' if type == Post.PostType.Request.value else 'A resident has applied to benifit from your offer'
        application = Application.objects.create(
            post=post,
            beneficiary=resident_profile,
            status=Application.ApplicationStatus.Pending.value,
            description=description
        )
        return application

    @staticmethod
    def cancel_post_application(resident_profile: ResidentProfile, application: Application) -> Application:
        """
        This is performed by the beneficiary
        """
        # Owner can cancel if accepted
        # Beneficiary can cancel if pending
        if application.post.owner == resident_profile:
            if application.status != Application.ApplicationStatus.Accepted.value:
                raise APIError(Error.CANNOT_CANCEL)
        else:
            if application.status != Application.ApplicationStatus.Pending.value:
                raise APIError(Error.CANNOT_CANCEL)

        application.status = Application.ApplicationStatus.Cancelled.value
        application.save()
        return application

    @staticmethod
    def accept_post_application(resident_profile: ResidentProfile, application: Application) -> Application:
        """
        This is performed by the owner
        """
        # check if the resident is the owner
        if application.post.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        # Accept if pending only
        if application.status != Application.ApplicationStatus.Pending.value:
            raise APIError(Error.MUST_BE_PENDING)

        # Accpet the application
        application.status = Application.ApplicationStatus.Accepted.value
        application.save()

        # Reject all other applications
        post = application.post
        all_applications = queries.get_all_post_applications_by(post=post, beneficiary=None, status=None)
        other_applications = all_applications.exclude(id=application.id)
        for app in other_applications:
            app.status = Application.ApplicationStatus.Rejected.value
            app.save()
        return application

    @staticmethod
    def reject_post_application(resident_profile: ResidentProfile, application: Application) -> Application:
        """
        This is performed by the owner
        """
        # check if the resident is the owner
        if application.post.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        # Reject if pending only
        if application.status != Application.ApplicationStatus.Pending.value:
            raise APIError(Error.MUST_BE_PENDING)

        # Reject the application
        application.status = Application.ApplicationStatus.Rejected.value
        application.save()

        return application

    @staticmethod
    def complete_application(resident_profile: ResidentProfile, application: Application) -> Application:
        """
        This is performed by the owner
        """
        # check if the resident is the owner
        if application.post.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        # Complete if accepted only
        if application.status != Application.ApplicationStatus.Accepted.value:
            raise APIError(Error.MUST_BE_ACCEPTED)

        # Complete the application
        application.status = Application.ApplicationStatus.Completed.value
        application.save()

        # Deactivate the post
        post = application.post
        post.is_active = False
        post.save()
        return application

    @staticmethod
    def update_application(resident_profile: ResidentProfile, application: Application, action: str) -> Application:
        if action == 'accept':
            return PostService.accept_post_application(resident_profile, application)
        elif action == 'reject':
            return PostService.reject_post_application(resident_profile, application)
        elif action == 'cancel':
            return PostService.cancel_post_application(resident_profile, application)
        elif action == 'complete':
            return PostService.complete_application(resident_profile, application)
        else:
            raise APIError(Error.UNSUPPORTED_ACTION)
