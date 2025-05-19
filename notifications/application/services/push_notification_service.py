from typing import List

from notifications.application.ports.driven.firebase_repository_port import FirebaseRepositoryPort
from notifications.application.ports.driving.push_notification_service_port import PushNotificationServicePort
from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport


class PushNotificationService(PushNotificationServicePort):
    def __init__(
            self,
            firebase: FirebaseRepositoryPort,
    ):
        self.firebase = firebase

    def send_silent_notification(self, notification: Notification, token: str) -> NotificationReport:
        updated_notification = self.firebase.send_single_silent_notification(notification, token)
        return updated_notification

    def send_silent_bulk(self, notification: Notification, tokens: List[str]) -> NotificationReport:
        updated_notification = self.firebase.send_bulk_silent_notification(notification, tokens)
        return updated_notification

    def send(self, notification: Notification, recipient: str) -> NotificationReport:
        updated_notification = self.firebase.send_single_notification(notification, recipient)
        return updated_notification

    def send_bulk(self, notification: Notification, recipients: List[str]) -> NotificationReport:
        updated_notification = self.firebase.send_bulk_notification(notification, recipients)
        return updated_notification
