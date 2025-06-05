from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from notifications.application.ports.driving.push_notification_service_port import PushNotificationServicePort
from notifications.application.ports.driving.email_notification_service_port import EmailNotificationServicePort
from notifications.application.ports.driving.sms_notification_service_port import SMSNotificationServicePort
from notifications.driving.api_rest.v1.notification.mapper import NotificationAPIMapper
from notifications.driving.api_rest.v1.notification.models import NotificationDataRequest
from dependency_injector.wiring import inject, Provide
from notifications.infrastructure.di.notification.container import NotificationContainer

fcm_router = APIRouter()


@fcm_router.post('/notification/send')
@inject
async def send_notification(notification_request: NotificationDataRequest,
                            service: PushNotificationServicePort = Depends(Provide[NotificationContainer.service]),
                            mapper: NotificationAPIMapper = Depends(Provide[NotificationContainer.api_mapper])):
    notification = mapper.from_notification_dto_to_domain(notification_request)
    if len(notification.recipients) > 1:
        service.send_bulk(notification, notification.recipients)
    else:
        service.send(notification, notification.recipients[0])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=None
    )


email_router = APIRouter()


@email_router.post('/notification/send-email')
@inject
async def send_email_notification(
    notification_request: NotificationDataRequest,
    service: EmailNotificationServicePort = Depends(Provide[NotificationContainer.email_service]),
    mapper: NotificationAPIMapper = Depends(Provide[NotificationContainer.api_mapper]),
):
    notification = mapper.from_notification_dto_to_domain(notification_request)
    if len(notification.recipients) > 1:
        service.send_bulk(notification, notification.recipients)
    else:
        service.send(notification, notification.recipients[0])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=None
    )

sms_router = APIRouter()


@sms_router.post('/notification/send-sms')
@inject
async def send_sms_notification(
    notification_request: NotificationDataRequest,
    service: SMSNotificationServicePort = Depends(Provide[NotificationContainer.sms_service]),
    mapper: NotificationAPIMapper = Depends(Provide[NotificationContainer.api_mapper]),
):
    notification = mapper.from_notification_dto_to_domain(notification_request)
    if len(notification.recipients) > 1:
        service.send_bulk(notification, notification.recipients)
    else:
        service.send(notification, notification.recipients[0])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=None
    )
