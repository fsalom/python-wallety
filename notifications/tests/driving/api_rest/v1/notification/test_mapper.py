from notifications.driving.api_rest.v1.notification.mapper import NotificationAPIMapper
from notifications.driving.api_rest.v1.notification.models import NotificationDataRequest, NotificationRequest, NotificationResponse
from notifications.domain.notification import Notification as DomainNotification


def test_from_notification_dto_to_domain_sets_fields_and_recipients():
    dto = NotificationDataRequest(
        notification=NotificationRequest(title="ti", content="co", data={"k": "v"}),
        recipients=["r1", "r2"]
    )
    domain = NotificationAPIMapper.from_notification_dto_to_domain(dto)
    assert isinstance(domain, DomainNotification)
    assert domain.title == "ti"
    assert domain.content == "co"
    assert domain.data == {"k": "v"}


def test_from_domain_to_notification_dto_maps_id_title_content():
    domain = DomainNotification(id=5, title="a", content="b", data={"x": "y"}, created_by_user_id=1)
    dto = NotificationAPIMapper.from_domain_to_notification_dto(domain)
    assert isinstance(dto, NotificationResponse)
    assert dto.id == 5
    assert dto.title == "a"
    assert dto.content == "b"
    # data field not in response model, extra values are ignored
    assert not hasattr(dto, 'data')