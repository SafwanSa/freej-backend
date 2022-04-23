from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError
from apps.campus.models import Campus


def get_all_campus_posts(campus: Campus) -> Iterable[Post]:
    return Post.objects.filter(is_deleted=False, campus=campus).order_by('-created_at')


def get_campus_post_by_id(campus: Campus, id: int) -> Post:
    try:
        return Post.objects.get(id=id, campus=campus)
    except Post.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Post._meta.model_name])


def get_all_campus_offers(campus: Campus) -> Iterable[Post]:
    return get_all_campus_posts(campus=campus).filter(type=Post.PostType.Offer.value)


def get_all_campus_requests(campus: Campus) -> Iterable[Post]:
    return get_all_campus_posts(campus=campus).filter(type=Post.PostType.Request.value)


def get_post_reviews(post: Post) -> Iterable[Review]:
    return post.reviews.filter(is_deleted=False).order_by('-created_at')


def get_post_images(post: Post) -> Iterable[Review]:
    return post.images.filter(is_deleted=False).order_by('-created_at')


def get_review_by_id(id: int) -> Post:
    try:
        return Review.objects.get(id=id)
    except Review.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Review._meta.model_name])


def get_all_post_applications_by(post: Post, beneficiary: ResidentProfile = None,
                                 status: Application.ApplicationStatus = None) -> Iterable[Application]:
    applications = post.applications.filter(is_deleted=False)
    if beneficiary:
        applications = applications.filter(beneficiary=beneficiary)
    if status:
        applications = applications.filter(status=status.value)
    return applications.order_by('-created_at')


def get_application_by_id(id: int) -> Application:
    try:
        return Application.objects.get(id=id)
    except Application.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Application._meta.model_name])
