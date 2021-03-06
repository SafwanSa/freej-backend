from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from core.admin import BaseAdmin, BaseStackedInline, BaseTabularInline
from core import utils


class PostAdmin(BaseAdmin):
    class PostImageInline(BaseTabularInline):
        model = PostImage
        fields = ['image']

    class ApplicationInline(BaseTabularInline):
        model = Application
        fields = ['beneficiary', 'status', 'status_updated_at']
        readonly_fields = ['status_updated_at']

    class ReviewInline(BaseTabularInline):
        model = Review
        fields = ['reviewer', 'rating', 'comment']

    model = Post
    inlines = [PostImageInline, ApplicationInline, ReviewInline]
    list_display = [
        'id',
        utils.linkify_field('campus'),
        utils.linkify_field('owner'),
        'title',
        'type',
        'is_active',
        'created_at'
    ]
    list_filter = ['campus', 'type', 'is_active', 'created_at']
    search_fields = ['owner__user__username', 'campus__name_ar', 'campus__name_en']


class ApplicationAdmin(BaseAdmin):
    model = Application
    list_display = [
        'id',
        utils.linkify_field('post'),
        utils.linkify_field('beneficiary'),
        'status',
        'status_updated_at',
        'created_at'
    ]
    list_filter = ['post__campus', 'status', 'status_updated_at', 'created_at']
    search_fields = ['beneficiary__user__username', 'post__campus__name_ar', 'post__campus__name_en']


class ReviewAdmin(BaseAdmin):
    model = Review
    list_display = [
        'id',
        utils.linkify_field('post'),
        utils.linkify_field('reviewer'),
        'rating',
        'comment',
        'created_at'
    ]
    list_filter = ['post__campus', 'rating', 'created_at']
    search_fields = ['reviewer__user__username', 'post__campus__name_en', 'post__campus__name_ar']


admin.site.register(Post, PostAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Review, ReviewAdmin)
