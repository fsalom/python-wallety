from notifications.application.ports.driven.sms_repository_port import SMSRepositoryPort
from notifications.application.ports.driven.notification_repository_port import NotificationRepositoryPort


def test_sms_repository_port_inherits_notification_repository_port():
    """
    SMSRepositoryPort should extend the generic NotificationRepositoryPort without redeclaring methods.
    """
    assert issubclass(SMSRepositoryPort, NotificationRepositoryPort)