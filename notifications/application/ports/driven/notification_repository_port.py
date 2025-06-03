from abc import ABC, abstractmethod
from typing import List

from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport


class NotificationRepositoryPort(ABC):
    @abstractmethod
    def create_notification(self, notification: Notification) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def send(self, notification: Notification, recipient: str) -> NotificationReport:
        raise NotImplementedError

    @abstractmethod
    def send_bulk(self, notification: Notification, recipients: List[str]) -> NotificationReport:
        raise NotImplementedError
