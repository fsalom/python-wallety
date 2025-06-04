import os
from typing import List, Dict, Any

import requests

from notifications.application.ports.driven.notification_repository_port import NotificationRepositoryPort
from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport


class SMSRepositoryAdapter(NotificationRepositoryPort):
    """
    Driven adapter for sending SMS notifications via HTTP API.
    """
    def create_notification(self, notification: Notification) -> Notification:
        return notification

    def send(self, notification: Notification, recipient: str) -> NotificationReport:
        payload: Dict[str, Any] = {"message": notification.content}
        if notification.data:
            payload["data"] = notification.data
        return self._send_single(payload, notification, recipient)

    def send_bulk(self, notification: Notification, recipients: List[str]) -> NotificationReport:
        payload: Dict[str, Any] = {"message": notification.content}
        if notification.data:
            payload["data"] = notification.data
        return self._send_bulk(payload, notification, recipients)

    @staticmethod
    def _send_single(
        payload: Dict[str, Any],
        notification: Notification,
        recipient: str,
    ) -> NotificationReport:
        invalid_recipients: List[str] = []
        api_url = os.environ.get("SMS_API_URL", "http://localhost:8000/sms")
        api_key = os.environ.get("SMS_API_KEY")
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        try:
            response = requests.post(api_url, json={**payload, "to": recipient}, headers=headers)
            if 400 <= response.status_code < 500:
                print(f"Invalid phone number {recipient}: {response.status_code}")
                invalid_recipients.append(recipient)
            elif response.status_code >= 500:
                print(f"Failed to send SMS to {recipient}: {response.status_code}")
        except Exception as e:
            print(f"Failed to send SMS to {recipient}: {e}")
        return NotificationReport(
            notification=notification,
            sent_to_device_ids=[recipient],
            invalid_device_ids=invalid_recipients,
        )

    @staticmethod
    def _send_bulk(
        payload: Dict[str, Any],
        notification: Notification,
        recipients: List[str],
    ) -> NotificationReport:
        invalid_recipients: List[str] = []
        api_url = os.environ.get("SMS_API_URL", "http://localhost:8000/sms")
        api_key = os.environ.get("SMS_API_KEY")
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        for recipient in recipients:
            try:
                response = requests.post(api_url, json={**payload, "to": recipient}, headers=headers)
                if 400 <= response.status_code < 500:
                    invalid_recipients.append(recipient)
                elif response.status_code >= 500:
                    print(f"Failed to send SMS to {recipient}: {response.status_code}")
            except Exception as e:
                print(f"Failed to send SMS to {recipient}: {e}")
        return NotificationReport(
            notification=notification,
            sent_to_device_ids=recipients,
            invalid_device_ids=invalid_recipients,
        )