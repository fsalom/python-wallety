from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport
from notifications.application.services.push_notification_service import PushNotificationService
from notifications.application.ports.driven.firebase_repository_port import FirebaseRepositoryPort


class FakeFirebaseRepo(FirebaseRepositoryPort):
    def __init__(self):
        self.calls = []

    def send_single_notification(self, notification: Notification, recipient: str) -> NotificationReport:
        self.calls.append(("send_single_notification", notification, recipient))
        return NotificationReport(notification=notification, sent_to_device_ids=[recipient], invalid_device_ids=[])

    def send_bulk_notification(self, notification: Notification, recipients: list[str]) -> NotificationReport:
        self.calls.append(("send_bulk_notification", notification, recipients))
        return NotificationReport(notification=notification, sent_to_device_ids=recipients, invalid_device_ids=[])

    def send_single_silent_notification(self, notification: Notification, recipient: str) -> NotificationReport:
        self.calls.append(("send_single_silent_notification", notification, recipient))
        return NotificationReport(notification=notification, sent_to_device_ids=[recipient], invalid_device_ids=[])

    def send_bulk_silent_notification(self, notification: Notification, recipients: list[str]) -> NotificationReport:
        self.calls.append(("send_bulk_silent_notification", notification, recipients))
        return NotificationReport(notification=notification, sent_to_device_ids=recipients, invalid_device_ids=[])


def test_push_notification_service_delegates_to_firebase():
    notification = Notification(title="T", content="C", created_by_user_id=1)
    fake_repo = FakeFirebaseRepo()
    service = PushNotificationService(firebase=fake_repo)

    report_single = service.send(notification, "token1")
    assert report_single.sent_to_device_ids == ["token1"]

    report_bulk = service.send_bulk(notification, ["token1", "token2"])
    assert report_bulk.sent_to_device_ids == ["token1", "token2"]

    report_silent_single = service.send_silent_notification(notification, "token1")
    assert report_silent_single.sent_to_device_ids == ["token1"]

    report_silent_bulk = service.send_silent_bulk(notification, ["token1", "token2"])
    assert report_silent_bulk.sent_to_device_ids == ["token1", "token2"]

    expected_calls = [
        ("send_single_notification", notification, "token1"),
        ("send_bulk_notification", notification, ["token1", "token2"]),
        ("send_single_silent_notification", notification, "token1"),
        ("send_bulk_silent_notification", notification, ["token1", "token2"]),
    ]
    assert fake_repo.calls == expected_calls