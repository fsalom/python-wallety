import pytest

from notifications.application.ports.driven.notification_repository_port import NotificationRepositoryPort
from notifications.domain.notification import Notification


class DummyNotificationRepo(NotificationRepositoryPort):
    def create_notification(self, notification: Notification):
        return super().create_notification(notification)

    def send(self, notification: Notification, recipient: str):
        return super().send(notification, recipient)

    def send_bulk(self, notification: Notification, recipients: list[str]):
        return super().send_bulk(notification, recipients)


@pytest.mark.parametrize("method,args", [
    ("create_notification", (Notification(title="t", content="c", created_by_user_id=1),)),
    ("send", (Notification(title="t", content="c", created_by_user_id=1), "r1")),
    ("send_bulk", (Notification(title="t", content="c", created_by_user_id=1), ["r2", "r3"])),
])
def test_not_implemented_methods_raise(method, args):
    repo = DummyNotificationRepo()
    func = getattr(repo, method)
    with pytest.raises(NotImplementedError):
        func(*args)