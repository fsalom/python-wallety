from abc import ABC, abstractmethod
from typing import List

from notifications.application.ports.driving.notification_service_port import NotificationServicePort
from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport


class PushNotificationServicePort(NotificationServicePort):
    @abstractmethod
    def send_silent_notification(self, notification: Notification, recipient: str) -> NotificationReport:
        raise NotImplementedError

    @abstractmethod
    def send_silent_bulk(self, notification: Notification, recipients: List[str]) -> NotificationReport:
        raise NotImplementedError
