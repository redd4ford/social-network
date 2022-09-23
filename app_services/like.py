from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db.utils import IntegrityError
from injector import inject

from app_services.post import PostService
from domain.core.exceptions import (
    LikeAlreadyExistsError,
    LikeDoesNotExistError,
)
from domain.core.singleton_metaclass import Singleton
from domain.models import Like
from domain.repositories.like import LikeRepository


User = get_user_model()


class LikeService(metaclass=type(Singleton)):
    @inject
    def __init__(self, repo: LikeRepository = LikeRepository()):
        super().__init__()
        self.repo = repo

    def get_all(self) -> Optional[QuerySet[Like]]:
        return self.repo.get_all()

    def like(self, actor: User, post_id) -> Optional[Like]:
        post = PostService().get_by_id(post_id)
        try:
            return self.repo.create(
                data={
                    'user': actor,
                    'post': post,
                }
            )
        except IntegrityError:
            raise LikeAlreadyExistsError

    def unlike(self, actor: User, post_id) -> Optional[Like]:
        unliked = self.repo.delete_by_post_id_and_user_id(actor.id, post_id)
        if not unliked:
            raise LikeDoesNotExistError
        return unliked
