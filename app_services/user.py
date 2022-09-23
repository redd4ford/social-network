from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from injector import inject
from psycopg2 import IntegrityError

from domain.core.exceptions import ObjectDoesNotExistError
from domain.core.singleton_metaclass import Singleton
from domain.repositories import UserRepository

User = get_user_model()


class UserService(metaclass=type(Singleton)):
    @inject
    def __init__(self, repo: UserRepository = UserRepository()):
        super().__init__()
        self.repo = repo

    def get_by_id(self, user_id: str = None) -> Optional[User]:
        obj = self.repo.get_by_id(user_id)
        if not obj:
            raise ObjectDoesNotExistError(User, user_id)
        return obj

    def update(self, data: dict, user_id: str) -> Optional[User]:
        obj = self.repo.get_by_id(user_id)
        if not obj:
            raise ObjectDoesNotExistError(User, user_id)
        try:
            return self.repo.update(obj, data)
        except IntegrityError:
            raise ValidationError
