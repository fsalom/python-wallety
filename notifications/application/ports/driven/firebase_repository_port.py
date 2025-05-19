from abc import ABC, abstractmethod
from typing import List
from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport


class FirebaseRepositoryPort(ABC):
    """
    Driven port for sending push notifications via Firebase Cloud Messaging (FCM).
    """
    @abstractmethod
    def send_single_notification(self, notification: Notification, recipient: str) -> NotificationReport:
        """
        Send a visible notification (with title and body) to a single device token.
        """
        raise NotImplementedError

    @abstractmethod
    def send_single_silent_notification(self, notification: Notification, recipient: str) -> NotificationReport:
        """
        Send a silent (data-only) notification to a single device token.
        """
        raise NotImplementedError

    @abstractmethod
    def send_bulk_notification(self, notification: Notification, recipients: List[str]) -> NotificationReport:
        """
        Send a visible notification to multiple device tokens.
        """
        raise NotImplementedError

    @abstractmethod
    def send_bulk_silent_notification(self, notification: Notification, recipients: List[str]) -> NotificationReport:
        """
        Send a silent (data-only) notification to multiple device tokens.
        """
        raise NotImplementedError
