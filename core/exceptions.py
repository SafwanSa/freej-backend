from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied
from django.http import Http404

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.response import Response
from rest_framework import status
import json


class ApplicationError(Exception):
    def __init__(self, message, extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(exc.messages)

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    if isinstance(exc.detail, list):
        code = exc.detail[0].code
        if code is 'invalid':
            code = 0
        response.data = {
            "error": {
                "code": code,
                "messages": [str(exc.detail[0])]
            }
        }
    else:
        messages = []
        try:
            if exc.detail.get('code'):
                messages = ['Access Token is invalid!']
            else:
                for (key, value) in enumerate(exc.detail):
                    d = exc.detail[value][0]
                    if isinstance(d, dict):
                        message = str(f'{value}:')
                        for (key2, value2) in enumerate(d):
                            message += str(f'{value2}:{d[value2][0]}')
                    else:
                        message = str(f'{value}:{exc.detail[value][0]}')
                    messages.append(message)
            code = 0
        except BaseException:
            code = -403
            messages = [exc.detail]
        response.data = {
            "error": {
                "code": code,
                "messages": messages
            }
        }
    if code == -404:
        return Response(response.data, status=status.HTTP_404_NOT_FOUND)
    else:
        return response
