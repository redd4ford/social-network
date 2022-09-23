from typing import Optional

import psycopg2
from django.db.models import QuerySet

from domain.core.singleton_metaclass import Singleton
from domain.models.like import Like


class LikeRepository(metaclass=type(Singleton)):
    @classmethod
    def get_all(cls):
        return Like.objects.all()

    @classmethod
    def get_by_id(cls, like_id) -> Optional[Like]:
        try:
            return Like.objects.get(id=like_id)
        except Like.DoesNotExist:
            return None

    @classmethod
    def get_by_post(cls, post_id) -> QuerySet[Like]:
        return Like.objects.filter(post__id=post_id)

    @classmethod
    def get_by_post_id_and_user_id(cls, user_id, post_id) -> Optional[Like]:
        try:
            return Like.objects.get(post__id=post_id, user__id=user_id)
        except Like.DoesNotExist:
            return None

    def create(self, data: dict) -> Like:
        obj = Like(**data)
        self.save(obj)
        return obj

    @classmethod
    def save(cls, obj: Like, update_fields: Optional[list] = None) -> None:
        obj.save(update_fields=update_fields)

    def delete_by_post_id_and_user_id(self, user_id: str, post_id: str) -> Optional[Like]:
        obj = self.get_by_post_id_and_user_id(user_id, post_id)
        if obj:
            return self.delete_like(obj)
        else:
            return None

    @classmethod
    def delete_like(cls, obj: Like) -> Optional[Like]:
        try:
            obj.delete()
            return obj
        except psycopg2.IntegrityError:
            return None

    def delete_all_by_post(self, post_id: str) -> None:
        self.get_by_post(post_id).delete()
