from core.models import BaseModel
from django.db import models
from apps.account.models import User
from enum import Enum
from core import utils
from apps.campus.models import ResidentProfile


class Post(BaseModel):
    class PostType(Enum):
        Offer = 'offer'
        Request = 'request'
    campus = models.ForeignKey('campus.campus', on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(max_length=20, choices=utils.create_choices_from_enum(PostType))
    owner = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='created_posts')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class PostImage(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.URLField(max_length=1024)


class Review(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField(default=0)
    comment = models.TextField(null=True, blank=True)


class Application(BaseModel):
    class ApplicationStatus(Enum):
        Pending = 'pending'
        Accepted = 'accepted'
        Rejected = 'rejected'
        Cancelled = 'cancelled'
        Completed = 'completed'
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='applications')
    beneficiary = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='posts_applications')
    status = models.CharField(max_length=20, choices=utils.create_choices_from_enum(ApplicationStatus))
    status_updated_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
