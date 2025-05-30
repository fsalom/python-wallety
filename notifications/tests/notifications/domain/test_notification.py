import pytest
from pydantic import ValidationError
from notifications.domain.notification import Notification

def test_notification_defaults():
    notification = Notification(title="Test Title", content="Test Content", created_by_user_id=1)
    assert notification.id is None
    assert notification.data is None

@pytest.mark.parametrize("missing_field", ["title", "content", "created_by_user_id"])
def test_notification_missing_fields_raise(missing_field):
    kwargs = {"title": "T", "content": "C", "created_by_user_id": 1}
    kwargs.pop(missing_field)
    with pytest.raises(ValidationError):
        Notification(**kwargs)