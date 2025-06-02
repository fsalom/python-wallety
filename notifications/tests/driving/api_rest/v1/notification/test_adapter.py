import pytest

from notifications.driving.api_rest.v1.notification.adapter import send_notification
from notifications.driving.api_rest.v1.notification.models import NotificationDataRequest, NotificationRequest
from notifications.domain.notification import Notification as DomainNotification


class DummyService:
    def __init__(self):
        self.calls = []

    def send(self, notification, recipient: str):
        self.calls.append(("send", recipient))

    def send_bulk(self, notification, recipients: list[str]):
        self.calls.append(("send_bulk", tuple(recipients)))


class DummyMapper:
    def from_notification_dto_to_domain(self, dto: NotificationDataRequest):
        # create simple domain-like object with recipients attribute
        class DummyNotification:
            def __init__(self, recipients):
                self.recipients = recipients

        return DummyNotification(dto.recipients)


@pytest.mark.asyncio
@pytest.mark.parametrize("recipients,expected", [
    (["r1"], ("send", "r1")),
    (["r1", "r2"], ("send_bulk", ("r1", "r2")))
])
async def test_send_notification(recipients, expected):
    service = DummyService()
    mapper = DummyMapper()
    dto = NotificationDataRequest(
        notification=NotificationRequest(title="t", content="c"),
        recipients=recipients
    )
    response = await send_notification(dto, service=service, mapper=mapper)
    assert response.status_code == 200
    assert service.calls == [expected]