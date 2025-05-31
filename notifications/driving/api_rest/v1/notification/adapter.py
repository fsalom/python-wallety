from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from notifications.application.ports.driving.push_notification_service_port import PushNotificationServicePort
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
