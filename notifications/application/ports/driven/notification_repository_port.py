from abc import ABC, abstractmethod
from typing import List
from notifications.domain.notification import Notification


class NotificationRepositoryPort(ABC):
    @abstractmethod
    def create_notification(self, notification: Notification) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def send(self, notification: Notification, recipient: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_bulk(self, notification: Notification, recipients: List[str]) -> None:
        raise NotImplementedError
