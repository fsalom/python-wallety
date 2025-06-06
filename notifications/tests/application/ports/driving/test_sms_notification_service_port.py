from notifications.application.ports.driving.sms_notification_service_port import SMSNotificationServicePort
from notifications.application.ports.driving.notification_service_port import NotificationServicePort


def test_sms_service_port_inherits_notification_service_port():
    """
    SMSNotificationServicePort should extend NotificationServicePort.
    """
    assert issubclass(SMSNotificationServicePort, NotificationServicePort)