from typing import List

from notifications.application.ports.driving.sms_notification_service_port import SMSNotificationServicePort
from notifications.application.ports.driven.sms_repository_port import SMSRepositoryPort
from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport


class SMSNotificationService(SMSNotificationServicePort):
    """
    Application service for sending SMS notifications.
    """
    def __init__(self, sms_repository: SMSRepositoryPort):
        self.sms_repository = sms_repository

    def send(self, notification: Notification, recipient: str) -> NotificationReport:
        return self.sms_repository.send(notification, recipient)

    def send_bulk(self, notification: Notification, recipients: List[str]) -> NotificationReport:
        return self.sms_repository.send_bulk(notification, recipients)