from typing import Optional

import psycopg2
from django.db.models import QuerySet

from domain.core.singleton_metaclass import Singleton
from domain.models import Post


class PostRepository(metaclass=type(Singleton)):
    @classmethod
    def get_all(cls) -> QuerySet[Post]:
        return Post.objects.all()

    @classmethod
    def get_by_id(cls, object_id: str) -> Optional[Post]:
        try:
            return Post.objects.get(id=object_id)
        except Post.DoesNotExist:
            return None

    @classmethod
    def get_by_user(cls, user_id: str) -> QuerySet[Post]:
        return Post.objects.filter(creator__id=user_id)

    def create(self, data: dict) -> Post:
        obj = Post(**data)
        self.save(obj)
        return obj

    def update(self, obj: Post, data: dict) -> Post:
        for name, value in data.items():
            setattr(obj, name, value)
        self.save(obj)
        return obj

    @classmethod
    def save(cls, obj: Post, update_fields: Optional[list] = None) -> None:
        obj.save(update_fields=update_fields)

    def delete_by_id(self, object_id: str) -> Optional[Post]:
        obj = self.get_by_id(object_id)
        return self.delete_post(obj)

    @classmethod
    def delete_post(cls, obj: Post) -> Optional[Post]:
        try:
            obj.delete()
            return obj
        except psycopg2.IntegrityError:
            return None

    def delete_all(self) -> None:
        self.get_all().delete()

    def delete_all_by_user(self, user_id: str) -> None:
        self.get_by_user(user_id).delete()
