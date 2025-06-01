import pytest

from notifications.application.ports.driving.notification_service_port import NotificationServicePort
from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport


class DummyServicePort(NotificationServicePort):
    def send(self, notification: Notification, recipient: str) -> NotificationReport:
        return super().send(notification, recipient)

    def send_bulk(self, notification: Notification, recipients: list[str]) -> NotificationReport:
        return super().send_bulk(notification, recipients)


@pytest.mark.parametrize("method,args", [
    ("send", (Notification(title="t", content="c", created_by_user_id=1), "r1")),
    ("send_bulk", (Notification(title="t", content="c", created_by_user_id=1), ["r2", "r3"])),
])
def test_notification_service_port_not_implemented(method, args):
    service = DummyServicePort()
    func = getattr(service, method)
    with pytest.raises(NotImplementedError):
        func(*args)