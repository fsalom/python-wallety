from abc import ABC, abstractmethod

from wallety.domain.entities.user import User


class UserRepositoryPort(ABC):
    @abstractmethod
    def create(self, user: User):
        pass

    @abstractmethod
    def list_users(self) -> [User]:
        pass