from apps.utility.models import BaseModel
from django.db import models
from apps.account.models import User
from enum import Enum
from core import utils
from apps.campus.models import ResidentProfile


class Post(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='created_posts')
    # TODO: images =

    class Meta:
        abstract = True


class Offer(Post):
    rating = models.FloatField(default=0)
    num_of_raters = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
