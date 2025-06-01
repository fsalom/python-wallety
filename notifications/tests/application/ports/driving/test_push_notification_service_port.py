import pytest

from notifications.application.ports.driving.push_notification_service_port import PushNotificationServicePort
from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport


class DummyPushPort(PushNotificationServicePort):
    def send(self, notification: Notification, recipient: str) -> NotificationReport:
        return super().send(notification, recipient)

    def send_bulk(self, notification: Notification, recipients: list[str]) -> NotificationReport:
        return super().send_bulk(notification, recipients)

    def send_silent_notification(self, notification: Notification, recipient: str) -> NotificationReport:
        return super().send_silent_notification(notification, recipient)

    def send_silent_bulk(self, notification: Notification, recipients: list[str]) -> NotificationReport:
        return super().send_silent_bulk(notification, recipients)


@pytest.mark.parametrize("method,args", [
    ("send_silent_notification", (Notification(title="t", content="c", created_by_user_id=1), "r1")),
    ("send_silent_bulk", (Notification(title="t", content="c", created_by_user_id=1), ["r2", "r3"])),
])
def test_push_notification_service_port_not_implemented(method, args):
    port = DummyPushPort()
    func = getattr(port, method)
    with pytest.raises(NotImplementedError):
        func(*args)