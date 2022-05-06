from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError
from apps.announcement import queries as announcementQueries
from apps.event import queries as eventQueries
from apps.post import queries as postQueries


def get_report_instance(report: Report) -> BaseModel:
    id = report.instance_id
    type = report.instance_type
    if type == Report.InstanceType.Announcement.value:
        return announcementQueries.get_announcement_by_id(id=id, with_deleted=True)
    elif type == Report.InstanceType.Post.value:
        return postQueries.get_post_by_id(id=id, with_deleted=True)
    elif type == Report.InstanceType.Event.value:
        return eventQueries.get_event_by_id(id=id, with_deleted=True)
    else:
        raise ValueError()
