from dependency_injector import containers, providers

from notifications.application.services.push_notification_service import PushNotificationService
from notifications.application.services.email_notification_service import EmailNotificationService
from notifications.application.services.sms_notification_service import SMSNotificationService
from notifications.driven.firebase.adapter import FirebaseRepositoryAdapter
from notifications.driven.email.adapter import EmailRepositoryAdapter
from notifications.driven.sms.adapter import SMSRepositoryAdapter
from notifications.driving.api_rest.v1.notification.mapper import NotificationAPIMapper


class NotificationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        modules=["notifications.driving.api_rest.v1.notification.adapter"]
    )

    firebase_repository = providers.Factory(FirebaseRepositoryAdapter)
    email_repository = providers.Factory(EmailRepositoryAdapter)
    sms_repository = providers.Factory(SMSRepositoryAdapter)

    service = providers.Factory(
        PushNotificationService,
        firebase=firebase_repository,
    )
    email_service = providers.Factory(
        EmailNotificationService,
        email_repository=email_repository,
    )
    sms_service = providers.Factory(
        SMSNotificationService,
        sms_repository=sms_repository,
    )

    api_mapper = providers.Factory(
        NotificationAPIMapper
    )