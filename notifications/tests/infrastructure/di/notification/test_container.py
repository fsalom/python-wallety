import pytest

from notifications.infrastructure.di.notification.container import NotificationContainer
from notifications.application.services.push_notification_service import PushNotificationService
from notifications.driven.firebase.adapter import FirebaseRepositoryAdapter
from notifications.driving.api_rest.v1.notification.mapper import NotificationAPIMapper


def test_container_providers_return_expected_instances():
    container = NotificationContainer()
    # firebase_repository provider
    firebase = container.firebase_repository()
    assert isinstance(firebase, FirebaseRepositoryAdapter)

    # service provider wiring firebase repository
    service = container.service()
    assert isinstance(service, PushNotificationService)
    assert isinstance(service.firebase, FirebaseRepositoryAdapter)

    # api_mapper provider
    mapper = container.api_mapper()
    assert isinstance(mapper, NotificationAPIMapper)