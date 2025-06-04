import pytest

from notifications.application.ports.driven.email_repository_port import EmailRepositoryPort
from notifications.application.ports.driven.notification_repository_port import NotificationRepositoryPort


def test_email_repository_port_inherits_notification_repository_port():
    """
    EmailRepositoryPort should extend the generic NotificationRepositoryPort without redeclaring methods.
    """
    assert issubclass(EmailRepositoryPort, NotificationRepositoryPort)