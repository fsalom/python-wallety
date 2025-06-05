from typing import List

from notifications.application.ports.driving.email_notification_service_port import EmailNotificationServicePort
from notifications.application.ports.driven.email_repository_port import EmailRepositoryPort
from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport


class EmailNotificationService(EmailNotificationServicePort):
    """
    Application service for sending email notifications.
    """
    def __init__(self, email_repository: EmailRepositoryPort):
        self.email_repository = email_repository

    def send(self, notification: Notification, recipient: str) -> NotificationReport:
        return self.email_repository.send(notification, recipient)

    def send_bulk(
        self, notification: Notification, recipients: List[str]
    ) -> NotificationReport:
        return self.email_repository.send_bulk(notification, recipients)