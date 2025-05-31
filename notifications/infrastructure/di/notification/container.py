from dependency_injector import containers, providers

from notifications.application.services.push_notification_service import PushNotificationService
from notifications.driven.firebase.adapter import FirebaseRepositoryAdapter
from notifications.driving.api_rest.v1.notification.mapper import NotificationAPIMapper


class NotificationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        modules=["notifications.driving.api_rest.v1.notification.adapter"]
    )

    firebase_repository = providers.Factory(FirebaseRepositoryAdapter)

    service = providers.Factory(
        PushNotificationService,
        firebase=firebase_repository,
    )

    api_mapper = providers.Factory(
        NotificationAPIMapper
    )