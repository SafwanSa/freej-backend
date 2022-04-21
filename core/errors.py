from typing import Iterable
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from enum import Enum


class Error(Enum):
    DEFAULT = {"code": -100, "detail": _("Oops!. Something went wrong, please contact us")}
    _DEFAULT_MESSAGE = {"code": 0, "detail": _("Default: {}")}
    INSTANCE_NOT_FOUND = {'code': -404, 'detail': _('{} not found!')}
    INVALID_JWT_TOKEN = {'code': -100, 'detail': _('Invalid token!')}
    REQUIRED_FIELD = {'code': 0, 'detail': _('This field is required!')}
    DATA_IS_MISSING = {'code': -101, 'detail': _('Data is missing!')}
    INVALID_TOKEN_OR_OTP = {'code': -460, 'detail': _("Invalid token or otp!")}
    EXPIRED_TOKEN = {'code': -460, 'detail': _("Your token has expired!")}
    NO_ACTIVE_ACCOUNT = {'code': -500, 'detail': _('No active account found with the given credentials!')}
    BLOCKED_USER = {'code': -403, 'detail': _('User is banned!')}
    # ACCOUNT_ALREADY_EXIST = {'code': -408, 'detail': _('Account with this mobile number or email already exist!')}
    INVALID_OTP = {'code': -408, 'detail': _('OTP is invalid!')}
    UNSUPPORTED_LANGUAGE = {'code': -487, 'detail': _('Provided language is unsupported!')}
    NOT_ALLOWED_TO_REQUEST_OTP = {'code': -478, 'detail': _('You have already requested an OTP, please wait!')}
    INVALID_DOMAIN = {
        'code': -788,
        'detail': _("Your email's domain does not match with selected campus domain!")}
    ACCOUNT_ALREADY_EXIST = {'code': -408, 'detail': _('Account with this email already exist!')}
    EVENT_HOST_ONLY = {'code': -569, 'detail': _("Only event's host can perform this action!")}
    NO_EVENT_APPLICATION = {'code': -560, 'detail': _("You did not apply for this event!")}
    NOT_OWNER = {'code': -365, 'detail': _("Only the owner can perform this action!")}
    ALREADY_RATED = {'code': -325, 'detail': _("You have already rated this post!")}
    ALREADY_APPLIED = {'code': -328, 'detail': _("You have already applied to this post!")}
    OWNER_CANNOT_APPLY = {'code': -477, 'detail': _("You cannot apply to your own post!")}
    CANNOT_CANCEL = {'code': -417, 'detail': _("You cannot cancel your application!")}


class APIError(Exception):
    def __init__(self, error: Error, extra=None):
        self.extra = extra or {}
        self.error = error
        self.extra = extra or None
        error_detail = error.value
        if self.extra:
            # Extra values can be used in foramtting a string that contains {}
            if isinstance(self.extra, list):
                error_detail['detail'] = error_detail['detail'].format(*extra)

        # try:
        #     logger.info(error.value)
        # except BaseException:
        #     pass
        super().__init__(error_detail)
