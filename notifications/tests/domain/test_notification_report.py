from notifications.domain.notification import Notification
from notifications.domain.notification_report import NotificationReport

def test_notification_report_defaults():
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = NotificationReport(notification=notification)
    assert report.sent_to_device_ids is None
    assert report.invalid_device_ids is None

def test_notification_report_with_lists():
    notification = Notification(title="T", content="C", created_by_user_id=1)
    report = NotificationReport(
        notification=notification,
        sent_to_device_ids=["token1", "token2"],
        invalid_device_ids=["bad_token"],
    )
    assert report.sent_to_device_ids == ["token1", "token2"]
    assert report.invalid_device_ids == ["bad_token"]