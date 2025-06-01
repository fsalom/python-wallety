import pytest

from notifications.application.ports.driven.firebase_repository_port import FirebaseRepositoryPort
from notifications.domain.notification import Notification


class DummyFirebasePort(FirebaseRepositoryPort):
    def send_single_notification(self, notification: Notification, recipient: str):
        return super().send_single_notification(notification, recipient)

    def send_single_silent_notification(self, notification: Notification, recipient: str):
        return super().send_single_silent_notification(notification, recipient)

    def send_bulk_notification(self, notification: Notification, recipients: list[str]):
        return super().send_bulk_notification(notification, recipients)

    def send_bulk_silent_notification(self, notification: Notification, recipients: list[str]):
        return super().send_bulk_silent_notification(notification, recipients)


@pytest.mark.parametrize("method,args", [
    ("send_single_notification", (Notification(title="t", content="c", created_by_user_id=1), "r1")),
    ("send_single_silent_notification", (Notification(title="t", content="c", created_by_user_id=1), "r2")),
    ("send_bulk_notification", (Notification(title="t", content="c", created_by_user_id=1), ["r3", "r4"])),
    ("send_bulk_silent_notification", (Notification(title="t", content="c", created_by_user_id=1), ["r5"])),
])
def test_not_implemented_methods_raise(method, args):
    port = DummyFirebasePort()
    func = getattr(port, method)
    with pytest.raises(NotImplementedError):
        func(*args)