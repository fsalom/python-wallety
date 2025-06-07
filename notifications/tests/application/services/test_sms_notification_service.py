from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport
from notifications.application.services.sms_notification_service import SMSNotificationService
from notifications.application.ports.driven.sms_repository_port import SMSRepositoryPort


class FakeSMSRepo(SMSRepositoryPort):
    def __init__(self):
        self.calls = []

    def create_notification(self, notification: Notification) -> Notification:
        return notification

    def send(self, notification: Notification, recipient: str) -> NotificationReport:
        self.calls.append(("send", notification, recipient))
        return NotificationReport(
            notification=notification,
            sent_to_device_ids=[recipient],
            invalid_device_ids=[],
        )

    def send_bulk(self, notification: Notification, recipients: list[str]) -> NotificationReport:
        self.calls.append(("send_bulk", notification, recipients))
        return NotificationReport(
            notification=notification,
            sent_to_device_ids=recipients,
            invalid_device_ids=[],
        )


def test_sms_notification_service_delegates_to_repository():
    notification = Notification(title="T", content="C", created_by_user_id=1)
    fake_repo = FakeSMSRepo()
    service = SMSNotificationService(sms_repository=fake_repo)

    report_single = service.send(notification, "12345")
    assert report_single.sent_to_device_ids == ["12345"]

    report_bulk = service.send_bulk(notification, ["123", "456"])
    assert report_bulk.sent_to_device_ids == ["123", "456"]

    assert fake_repo.calls == [
        ("send", notification, "12345"),
        ("send_bulk", notification, ["123", "456"]),
    ]