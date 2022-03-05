from typing import Iterable
from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied
from django.http import Http404
from rest_framework.exceptions import ValidationError as SerializerValidationError
from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.response import Response
from rest_framework import status
import json
from django.utils.translation import gettext_lazy as _
from core.errors import APIError


# class ApplicationError(Exception):
#     def __init__(self, message, extra=None):
#         super().__init__(message)

#         self.message = message
#         self.extra = extra or {}


def return_error_response(code: int, messages: Iterable[str]) -> dict:
    data = {
        "error": {
            "code": code,
            "messages": messages
        }
    }
    if code == -404 or code == 404:
        sts = status.HTTP_404_NOT_FOUND
    elif code == -403 or code == 403:
        sts = status.HTTP_403_FORBIDDEN
    elif code == -401 or code == 401:
        sts = status.HTTP_401_UNAUTHORIZED

    else:
        sts = status.HTTP_400_BAD_REQUEST
    return Response(data, status=sts)


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(exc.messages)

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    if response is None:
        if isinstance(exc, APIError):
            error = exc.error.value
            return return_error_response(code=error['code'], messages=[error['detail']])
        return response

    if isinstance(exc, SerializerValidationError):
        code = -400
        messages = []
        try:
            for key, value in exc.detail.items():
                d = value[0]
                if isinstance(d, dict):
                    message = str(f'{value}:')
                    for (key2, value2) in enumerate(d):
                        message += str(f'{value2}:{d[value2][0]}')
                else:
                    message = str(f'{key}:{str(value[0])}')
                    if 'non_field_errors:' in message:
                        message = message.replace('non_field_errors:', '')
                # if ':' in message:
                #     field_name = message.split(':')[0]
                #     error_message = message.split(':')[1]
                #     if 'This' in error_message:
                #         error_message = error_message.replace('This value', field_name.replace('_', ' '))
                #     message = error_message
                messages.append(message)
        except BaseException:
            code = -403
            messages = [exc.detail]
        return return_error_response(code=code, messages=messages)
    else:
        code = exc.status_code
        code = (code * -1) if code > 0 else code
        message = str(exc.detail)
        if isinstance(exc.detail, dict):
            if exc.detail.get('code'):
                message = _('Token is invalid!')
        return return_error_response(code=code, messages=[message])
