from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from django.contrib.auth import password_validation
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User
from apps.campus import queries as campusQueries
from apps.campus.models import Campus
import json


class AccountService:

    @staticmethod
    def does_account_exist(username: str) -> bool:
        users = queries.get_users_with(username=username)
        return users.exists()

    @staticmethod
    def validate_domain(email: str, campus: Campus) -> None:
        user_domain = email.split('@')[1]
        campus_domain = campus.email_domain
        if campus_domain and user_domain != campus_domain:
            raise APIError(Error.INVALID_DOMAIN)

    @staticmethod
    def register_resident(email: str, password: str, room_id: int, name: str,
                          mobile_number: str, send_otp: bool = True) -> OTP:
        # Check if user exists
        account_exist = AccountService.does_account_exist(username=email)
        if account_exist:
            raise APIError(Error.ACCOUNT_ALREADY_EXIST)

        # Get room. if not exist, raise an error
        room = campusQueries.get_room_by_id(id=room_id)
        # If the campus has a domain, validate it against the user's email
        AccountService.validate_domain(email=email, campus=room.building.campus)
        # Validate password
        dummy_account = User(
            username=email,
            is_superuser=False
        )
        password_validation.validate_password(password, dummy_account)

        # Request OTP
        if send_otp:
            otp = AuthService.request_otp(username=email)
            return otp
        return None

    @staticmethod
    def create_account(username: str, password: str, name: str, mobile_number: str) -> User:
        new_account = User(
            username=username,
            first_name=name,
            mobile_number=mobile_number,
            is_superuser=False,
        )
        password_validation.validate_password(password, new_account)
        new_account.set_password(password)
        new_account.is_active = True
        new_account.is_email_verified = True
        new_account.save()
        return new_account

    @staticmethod
    def get_or_create_fcm_token(user: User, token: str, is_active: bool) -> FCMToken:
        """
        This function does two things:
            1- Activate or create activated FCM Token
            2- Deactivate or create deactivated FCM Token

        Args:
            user (User): User instance
            token (str): FCM Token
            is_active (bool): If True, option 1, else option 2

        Returns:
            FCMToken: FCMToken instance
        """
        try:
            fcmToken = queries.get_fcm_token_with(user=user, token=token)
            if fcmToken.is_active != is_active:
                fcmToken.is_active = is_active
                fcmToken.save()
            return fcmToken
        except FCMToken.DoesNotExist:
            new_token = FCMToken(token=token, user=user, is_active=is_active)
            new_token.save()
            return new_token


class AuthService:

    @staticmethod
    def is_allowed_to_request_otp(username: str) -> bool:
        otps = queries.get_active_requested_otps_of(username=username)
        active_otp_exist = False
        for otp in otps.filter():
            not_expired_otp = otp.expiration_date > timezone.now()
            recently_requested_otp = (otp.created_at + timedelta(seconds=Conf.OTP_WAITING_PERIOD())) > timezone.now()
            if recently_requested_otp and not_expired_otp:
                active_otp_exist = True

        return not active_otp_exist

    @staticmethod
    def request_otp(username: str) -> OTP:
        # NOTE: To prevent users from requesting too many otps, the frontend should also control this behavior
        # Prevent requesting otps over and over with the time limit (Conf.OTP_WAITING_PERIOD)
        is_allowed_to_request_otp = AuthService.is_allowed_to_request_otp(username=username)
        if not is_allowed_to_request_otp:
            raise APIError(Error.NOT_ALLOWED_TO_REQUEST_OTP)
        # Deactivate old ones
        otps = queries.get_active_requested_otps_of(username=username)
        for otp in otps:
            otp.is_active = False
            otp.save()
        # Create a new one
        new_otp = OTP.objects.create(username=username)
        NotificationService.send(
            type=NotificationType.Email,
            template='email/otp.html',
            title='Your freej OTP',
            receivers=username,
            data=json.dumps({
                "email": username,
                "otp": new_otp.otp
            })
        )
        return new_otp

    @staticmethod
    def check_otp(username: str, otp: str) -> OTP:
        try:
            otp = queries.get_active_otp_with(username, otp)
            return otp
        except OTP.DoesNotExist:
            raise APIError(Error.INVALID_OTP)

    @staticmethod
    def generate_check_otp_token(otp: OTP) -> str:
        token = utils.generate_token(seconds_exp=600, type='otp_check', payload={'otp_id': otp.id})
        return token

    @staticmethod
    def optain_resident_access_token(user: User, token: dict) -> dict:
        if not user.groups.filter(name=GroupEnum.Resident.value).exists():
            raise APIError(Error.NO_ACTIVE_ACCOUNT)
        token['roles'] = list(user.groups.all().values())
        return token

    @staticmethod
    def optain_access_token(group: GroupEnum, user: User, token: dict) -> dict:
        if user.is_blocked:
            raise APIError(Error.BLOCKED_USER)

        if group == GroupEnum.Resident:
            return AuthService.optain_resident_access_token(user=user, token=token)
        else:
            raise APIError(Error.NO_ACTIVE_ACCOUNT)

    @staticmethod
    def request_change_password_otp(username: str) -> OTP:
        account_exist = AccountService.does_account_exist(username=username)
        otp = None
        if account_exist:
            otp = AuthService.request_otp(username=username)
        return otp

    @staticmethod
    def change_password(username: str, new_password: str, token: str) -> User:
        try:
            payload = utils.decode_jwt(token=token)
            otp = queries.get_otp_by_id(id=payload.get('otp_id'))
            if not otp.is_active or otp.username != username:
                raise APIError(Error.INVALID_TOKEN_OR_OTP)
        except Exception:
            raise APIError(Error.INVALID_JWT_TOKEN)
        user = queries.get_users_with(username=username).first()
        if user:
            password_validation.validate_password(new_password, user)
            user.set_password(new_password)
            user.save()
        otp.is_active = False
        otp.save()
        return user
