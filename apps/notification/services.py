from .models import *
from . import queries
from apps.utility.services import ConfigService as Conf
from django.core.mail import EmailMultiAlternatives
import json
from django.template.loader import get_template
from django.conf import settings
import urllib
from django.core.exceptions import ValidationError
from django.template import TemplateDoesNotExist
from django.core.validators import validate_email
import re
from core.validators import _PHONE_REGEX
from enum import Enum
from pyfcm import FCMNotification
from apps.account import queries as accountQueries


class NotificationType(Enum):
    SMS = 'SMS'
    Email = 'Email'
    PushNotification = 'PushNotification'


class NotificationService:

    @staticmethod
    def send(
        type: Notification.NotificationType,
        receivers: str,
        title: str = None,
        body: str = None,
        data: dict = None,
        template: str = None,
        extra: dict = None
    ) -> Notification:
        if type == Notification.NotificationType.Email:
            nf = Notification(
                type='Email',
                receivers=receivers,
                title=title,
                template=template,
                data=data,
            )
            if Conf.ACTIVATE_EMAILS():
                nf.result = NotificationService.send_email_notification(
                    title=title,
                    template=template,
                    data=data,
                    receivers=receivers
                )
            nf.save()

        elif type == Notification.NotificationType.SMS:
            nf = Notification(
                type='SMS',
                receivers=receivers,
                body=body
            )
            if Conf.ACTIVATE_SMS:
                nf.result = NotificationService.send_sms_notification(
                    receivers,
                    body
                )
            nf.save()

        elif type == Notification.NotificationType.PushNotification:
            nf = Notification(
                type=Notification.NotificationType.PushNotification.value,
                title=title,
                receivers=receivers,
                body=body
            )
            usernames = receivers.split(',')
            tokens = accountQueries.get_active_tokens_with(usernames=usernames)
            if tokens.exists():
                fcms = tokens.values_list('token', flat=True)[::1]
            else:
                fcms = []
            push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)
            nf.result = push_service.notify_multiple_devices(
                registration_ids=fcms,
                message_title=title,
                message_body=body,
                badge=1
            )
            nf.save()

        else:
            raise ValidationError('Unsupported notification type!')

    def send_email_notification(
        receivers: str,
        title: str,
        template: str,
        data: dict = None,
        bcc: list = None
    ) -> str:
        def is_valid(email: str) -> bool:
            try:
                validate_email(email)
                return True
            except ValidationError:
                return False
        try:
            # receivers supposed to be a CSV field
            receivers_list = receivers.split(',')
            receivers_list = [
                email for email in receivers_list if is_valid(email)]

            plaintext = get_template(template)
            html = get_template(template)
            subject = title
            data = json.loads(data)

            msg = EmailMultiAlternatives(
                subject, plaintext.render(data),
                settings.DEFAULT_FROM_EMAIL,
                receivers_list,
                bcc=bcc,
            )

            msg.attach_alternative(html.render(data), "text/html")
            return msg.send()
        except TemplateDoesNotExist:
            raise ValidationError('Template does not exist!')

    def send_sms_notification(
        receivers: str,
        body: str
    ) -> str:
        def is_valid(mobile: str):
            return re.fullmatch(_PHONE_REGEX.regex, mobile)

        receivers_list = receivers.split(',')
        receivers_list = [
            mobile for mobile in receivers_list if is_valid(mobile)]
        # Integrate here with any SMS provider
        # NOTE u have to return the response of the request
        """
        url = 'http://basic.unifonic.com/rest/SMS/messages'
        arr_data = {
            'AppSid': settings.UNIFONIC_APPSID,
            'SenderID': settings.UNIFONIC_SENDER_ID,
            'Body': body,
            'Recipient': receivers_list,
        }
        data = urllib.parse.urlencode(arr_data).encode('utf-8')
        response = urllib.request.urlopen(url=url, data=data)
        return response.read()
        """
