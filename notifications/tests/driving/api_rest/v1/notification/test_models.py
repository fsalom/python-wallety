import pytest

from pydantic import ValidationError

from notifications.driving.api_rest.v1.notification.models import (
    FirebaseDeviceId, PlatformDevice,
    NotificationRequest, NotificationDataRequest, NotificationResponse
)


def test_firebase_device_id_valid_and_invalid():
    # valid token of required length and pattern (22 chars + ':' + 140 chars)
    token = 'A' * 22 + ':' + 'B' * 140
    from pydantic import BaseModel

    class M(BaseModel):
        id: FirebaseDeviceId

    # valid assignment
    m = M(id=token)
    assert m.id == token
    # invalid token should raise ValidationError
    with pytest.raises(ValidationError):
        M(id='invalid_token')


def test_platform_device_literal():
    # allow specified literal values via pydantic validation
    from pydantic import BaseModel

    class M2(BaseModel):
        platform: PlatformDevice

    m2 = M2(platform='ios')
    assert m2.platform == 'ios'
    m2 = M2(platform='android')
    assert m2.platform == 'android'
    with pytest.raises(ValidationError):
        M2(platform='windows')


def test_notification_request_and_response_models():
    # minimal request
    req = NotificationRequest(title='t', content='c')
    assert req.id is None
    assert req.data is None
    # populate all fields
    req2 = NotificationRequest(id=7, title='a', content='b', data={'x': 1})
    assert req2.id == 7
    assert req2.data == {'x': 1}

    # data request includes recipients
    data_req = NotificationDataRequest(notification=req, recipients=['r'])
    assert data_req.notification is req
    assert data_req.recipients == ['r']

    # NotificationResponse has id, title, content only
    resp = NotificationResponse(id=3, title='ti', content='co')
    assert resp.id == 3
    assert resp.title == 'ti'
    assert resp.content == 'co'
    with pytest.raises(ValidationError):
        NotificationResponse(id='x', title=1, content=2)