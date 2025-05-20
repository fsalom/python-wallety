from typing import Optional, List
from pydantic import BaseModel
from notifications.domain.notification import Notification


class NotificationReport(BaseModel):
    notification: Notification
    sent_to_device_ids: Optional[List[str]] = None
    invalid_device_ids: Optional[List[str]] = None
