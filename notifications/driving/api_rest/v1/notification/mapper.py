from notifications.domain.notification import Notification
from notifications.driving.api_rest.v1.notification.models import NotificationResponse, NotificationDataRequest


class NotificationAPIMapper:
    @staticmethod
    def from_notification_dto_to_domain(dto: NotificationDataRequest) -> Notification:
        return Notification(
            content=dto.notification.content,
            title=dto.notification.title,
            data=dto.notification.data,
            created_by_user_id=0,
        )

    @staticmethod
    def from_domain_to_notification_dto(domain: Notification) -> NotificationResponse:
        return NotificationResponse(
            id=domain.id,
            content=domain.content,
            title=domain.title,
            data=domain.data,
        )
