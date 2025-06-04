from typing import List
import smtplib
from email.message import EmailMessage

from notifications.application.ports.driven.notification_repository_port import NotificationRepositoryPort
from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport


class EmailRepositoryAdapter(NotificationRepositoryPort):
    """
    Driven adapter for sending emails using smtplib and EmailMessage.
    """
    def create_notification(self, notification: Notification) -> Notification:
        return notification

    def send(self, notification: Notification, recipient: str) -> NotificationReport:
        msg = EmailMessage()
        msg['Subject'] = notification.title
        msg['To'] = recipient
        msg.set_content(notification.content)
        if notification.data:
            for key, value in notification.data.items():
                msg[key] = str(value)
        return self._send_single(msg, notification, recipient)

    def send_bulk(self, notification: Notification, recipients: List[str]) -> NotificationReport:
        msg = EmailMessage()
        msg['Subject'] = notification.title
        msg['To'] = ', '.join(recipients)
        msg.set_content(notification.content)
        if notification.data:
            for key, value in notification.data.items():
                msg[key] = str(value)
        return self._send_bulk(msg, notification, recipients)

    @staticmethod
    def _send_single(
        msg: EmailMessage,
        notification: Notification,
        recipient: str,
    ) -> NotificationReport:
        invalid_recipients: List[str] = []
        try:
            with smtplib.SMTP() as server:
                server.send_message(msg)
        except smtplib.SMTPRecipientsRefused:
            invalid_recipients.append(recipient)
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")
        return NotificationReport(
            notification=notification,
            sent_to_device_ids=[recipient],
            invalid_device_ids=invalid_recipients,
        )

    @staticmethod
    def _send_bulk(
        msg: EmailMessage,
        notification: Notification,
        recipients: List[str],
    ) -> NotificationReport:
        invalid_recipients: List[str] = []
        try:
            with smtplib.SMTP() as server:
                refused = server.send_message(msg)
                if refused:
                    invalid_recipients = list(refused.keys())
        except Exception as e:
            for recipient in recipients:
                print(f"Failed to send email to {recipient}: {e}")
        return NotificationReport(
            notification=notification,
            sent_to_device_ids=recipients,
            invalid_device_ids=invalid_recipients,
        )