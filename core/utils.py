import os
from typing import Iterable
import uuid
import jwt
from datetime import datetime, timedelta
import math
import random
from django.urls import reverse
from django.utils.html import format_html
from django.conf import settings
from rest_framework import serializers
from enum import Enum
from django.utils.deconstruct import deconstructible


class RandomFileName(object):
    """
        Random file names for user generated contents
    """

    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4(), ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


def generate_token(id: int, hours_expiry: int, type: str) -> str:
    payload = {
        "token_type": type,
        "exp": (datetime.now() + timedelta(hours=hours_expiry)).timestamp(),
        "user_id": id
    }
    return jwt.encode(payload, f"{settings.SECRET_KEY}", algorithm="HS256")


def generate_otp() -> str:
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def to_list(string: str) -> list:
    return string.replace(
        '[', '').replace(']', '').replace("'", '').replace(' ', '').split(',')


def to_string(_list: list) -> str:
    return '[' + ','.join(_list) + ']'


def linkify_field(field_name) -> str:
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """
    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


def linkify_instance(instance) -> str:
    """
    Converts an object into clickable links.
    Link will be admin url for the admin url for obj.parent.id:change
    """
    linked_obj = instance
    if linked_obj is None:
        return '-'
    app_label = linked_obj._meta.app_label
    model_name = linked_obj._meta.model_name
    view_name = f'admin:{app_label}_{model_name}_change'
    link_url = reverse(view_name, args=[linked_obj.pk])
    return format_html('<a href="{}">{}</a>', link_url, linked_obj)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` and 'exclude' argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            not_allowed = set(exclude)
            for exclude_name in not_allowed:
                self.fields.pop(exclude_name)


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer, ), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name='', fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def create_choices_from_enum(enum: Enum):
    choices = []
    for enum_value in enum:
        choices.append((enum_value.value, (enum(enum_value.value).name).replace('_', ' ')))
    return tuple(choices)
