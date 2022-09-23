from typing import Optional

from django.contrib.auth import get_user_model

from domain.core.singleton_metaclass import Singleton


User = get_user_model()


class UserRepository(metaclass=type(Singleton)):
    @classmethod
    def get_by_id(cls, obj_id: str) -> Optional[User]:
        try:
            return User.objects.get(id=obj_id)
        except User.DoesNotExistError:
            return None

    @classmethod
    def get_by_email(cls, email: str) -> Optional[User]:
        return User.objects.get(email=email)

    def update(self, obj, data: dict) -> User:
        for name, value in data.items():
            setattr(obj, name, value)
        self.save(obj)
        return obj

    @classmethod
    def save(cls, obj, update_fields: Optional[list] = None) -> None:
        obj.save(update_fields=update_fields)
