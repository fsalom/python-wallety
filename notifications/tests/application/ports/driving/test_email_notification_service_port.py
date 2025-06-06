from notifications.application.ports.driving.email_notification_service_port import EmailNotificationServicePort
from notifications.application.ports.driving.notification_service_port import NotificationServicePort


def test_email_service_port_inherits_notification_service_port():
    """
    EmailNotificationServicePort should extend NotificationServicePort.
    """
    assert issubclass(EmailNotificationServicePort, NotificationServicePort)