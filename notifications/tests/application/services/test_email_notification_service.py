from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport
from notifications.application.services.email_notification_service import EmailNotificationService
from notifications.application.ports.driven.email_repository_port import EmailRepositoryPort


class FakeEmailRepo(EmailRepositoryPort):
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

    def send_bulk(
        self, notification: Notification, recipients: list[str]
    ) -> NotificationReport:
        self.calls.append(("send_bulk", notification, recipients))
        return NotificationReport(
            notification=notification,
            sent_to_device_ids=recipients,
            invalid_device_ids=[],
        )


def test_email_notification_service_delegates_to_repository():
    notification = Notification(title="T", content="C", created_by_user_id=1)
    fake_repo = FakeEmailRepo()
    service = EmailNotificationService(email_repository=fake_repo)

    report_single = service.send(notification, "a@example.com")
    assert report_single.sent_to_device_ids == ["a@example.com"]

    report_bulk = service.send_bulk(notification, ["a@example.com", "b@example.com"])
    assert report_bulk.sent_to_device_ids == ["a@example.com", "b@example.com"]

    assert fake_repo.calls == [
        ("send", notification, "a@example.com"),
        ("send_bulk", notification, ["a@example.com", "b@example.com"]),
    ]