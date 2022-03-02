from .models import *
from . import queries
from enum import Enum
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


class NotificationType(Enum):
    SMS = 'SMS'
    Email = 'Email'


class NotificationService:

    @staticmethod
    def send(
        type: NotificationType,
        receivers: str,
        title: str = None,
        body: str = None,
        data: dict = None,
        template: str = None,
        extra: dict = None
    ) -> Notification:
        if type == NotificationType.Email:
            nf = Notification(
                type='Email',
                receivers=receivers,
                title=title,
                template=template,
                data=data,
            )
            nf.result = NotificationService.send_email_notification(
                title=title,
                template=template,
                data=data,
                receivers=receivers
            )
            nf.save()

        elif type == NotificationType.SMS:
            nf = Notification(
                type='SMS',
                receivers=receivers,
                body=body
            )
            nf.result = NotificationService.send_sms_notification(
                receivers,
                body
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
    ) -> None:
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
            msg.send()
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
