from typing import Iterable
from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User
from apps.campus.models import ResidentProfile, Campus


class PostService:

    @staticmethod
    def send_push_notification(post: Post, receivers: Iterable[ResidentProfile], title: str, body: str) -> None:
        if len(receivers) != 0:
            NotificationService.send(
                type=NotificationType.PushNotification,
                title=title,
                body=body,
                receivers=','.join([resident.user.username for resident in receivers]),
                data={
                    "type": "post",
                    "instance_id": post.id
                }
            )

    @staticmethod
    def rate_post(resident_profile: ResidentProfile, post: Post, rating: int, comment: str = None) -> Post:

        applications = queries.get_all_post_applications_by(
            post=post,
            beneficiary=resident_profile,
            status=Application.ApplicationStatus.Completed
        )
        if not applications.exists():
            raise APIError(Error.MUST_HAVE_COMPLETED_APP)

        reviews = queries.get_post_reviews(post=post)
        reviews = reviews.filter(reviewer=resident_profile)
        if reviews.exists():
            raise APIError(Error.ALREADY_RATED)

        new_review = Review.objects.create(
            post=post,
            reviewer=resident_profile,
            rating=rating,
            comment=comment
        )

        # Update resident profile
        owner = post.owner
        owner.num_of_raters += 1
        owner.rating = (owner.rating + rating) / owner.num_of_raters
        owner.save()
        # Send notification to the owner
        PostService.send_push_notification(
            post=post,
            receivers=[post.owner],
            title='You have been rated',
            body='{} has rated you for your {} ({})'.format(resident_profile.user.first_name, post.type, post.title),
        )

        return new_review

    @staticmethod
    def create_post(type: Post.PostType, resident_profile: ResidentProfile,
                    title: str, description: str, images: list = None) -> Post:
        campus = resident_profile.room.building.campus
        new_post = Post.objects.create(
            type=type.value,
            campus=campus,
            owner=resident_profile,
            title=title,
            description=description,
        )
        if images is not None and len(images) != 0:
            for url in images:
                new_image = PostImage.objects.create(
                    post=new_post,
                    image=url
                )
        return new_post

    @staticmethod
    def update_post(resident_profile: ResidentProfile, post: Post, is_active: bool = None,
                    title: str = None, description: str = None, images: list = None) -> Post:

        if post.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        if post:
            post.title = title
        if description:
            post.description = description
        if is_active is not None:
            post.is_active = is_active

        if images is not None and len(images) != 0:
            # Delete previous images
            old_images = queries.get_post_images(post=post)
            for img in old_images:
                img.delete()

            # Add new images
            for url in images:
                new_image = PostImage.objects.create(
                    post=post,
                    image=url
                )
        # Send notifications to all applicants
        beneficiaries = queries.get_post_active_beneficiaries(post=post)
        PostService.send_push_notification(
            post=post,
            receivers=beneficiaries,
            title='Applied {} ({}) is updated'.format(post.type, post.title),
            body='The {} you applied for has been updated'.format(post.type),
        )
        post.save()
        return post

    @staticmethod
    def delete_post(resident_profile: ResidentProfile, post: Post) -> Post:

        if post.owner != resident_profile:
            raise APIError(Error.NOT_OWNER)

        applications = queries.get_all_post_applications_by(post=post)
        found_non_deletable = False
        for app in applications:
            if app.status in [Application.ApplicationStatus.Accepted.value,
                              Application.ApplicationStatus.Completed.value]:
                found_non_deletable = True

        if found_non_deletable:
            raise APIError(Error.CANNOT_DELETE_POST)
        else:
            applications = applications.filter(status=Application.ApplicationStatus.Pending.value)
            for app in applications:
                app.status = Application.ApplicationStatus.Rejected.value
                app.save()

        # Send notifications to all applicants
        beneficiaries = queries.get_post_beneficiaries(post=post)
        PostService.send_push_notification(
            post=post,
            receivers=beneficiaries,
            title='Applied {} ({}) is deleted'.format(post.type, post.title),
            body='The {} you applied for has been deleted'.format(post.type),
        )
        post.delete()
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
        # Send notifications to owner
        PostService.send_push_notification(
            post=post,
            receivers=[post.owner],
            title='New applications for your {} ({})'.format(post.type, post.title),
            body='{} has applied to your {} ({})'.format(resident_profile.user.first_name, post.type, post.title),
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
        # Send notifications to applicant or owner
        if application.post.owner == resident_profile:
            PostService.send_push_notification(
                post=application.post,
                receivers=[application.beneficiary],
                title='Application has been cancelled',
                body='Your application to the {} ({}) has been cancelled'.format(
                    application.post.type, application.post.title),
            )
        else:
            PostService.send_push_notification(
                post=application.post,
                receivers=[application.post.owner],
                title='Application has been cancelled',
                body='An application for your {} ({}) has been cancelled by beneficiary'.format(
                    application.post.type, application.post.title),
            )
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

        # Reject all other applications if the post was a Request
        post = application.post
        if post.type == Post.PostType.Request.value:
            all_applications = queries.get_all_post_applications_by(post=post, beneficiary=None, status=None)
            other_applications = all_applications.exclude(id=application.id)
            for app in other_applications:
                app.status = Application.ApplicationStatus.Rejected.value
                app.save()
        # Send notifications to applicant
        PostService.send_push_notification(
            post=application.post,
            receivers=[application.beneficiary],
            title='Application has been accepted',
            body='Your application to the {} ({}) has been accepted, contact the owner'.format(
                application.post.type, application.post.title),
        )
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
        PostService.send_push_notification(
            post=application.post,
            receivers=[application.beneficiary],
            title='Application has been rejected',
            body='Your application to the {} ({}) has been rejected'.format(
                application.post.type, application.post.title),
        )
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
        # Send notifications to applicant
        PostService.send_push_notification(
            post=application.post,
            receivers=[application.beneficiary],
            title='Application has been completed',
            body='Your application to the {} ({}) is completed'.format(
                application.post.type, application.post.title),
        )
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
