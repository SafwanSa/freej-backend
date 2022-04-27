from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User
from apps.campus.models import ResidentProfile, Campus


class ReportService():

    @staticmethod
    def report_instance(resident_profile: ResidentProfile, instance_id: int,
                        instance_type: str, comment: str = None) -> Report:
        supported_type = Report.InstanceType.has_member_key(instance_type)
        if not supported_type:
            raise APIError(Error.UNSUPPORTED_REPORT_TYPE)

        new_report = Report.objects.create(
            reporter=resident_profile,
            instance_type=instance_type,
            instance_id=instance_id,
            comment=comment
        )
        return new_report
