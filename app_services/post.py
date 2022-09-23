from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from injector import inject
from psycopg2 import IntegrityError

from domain.core.exceptions import (
    ObjectDoesNotExistError,
    UserNotAuthorizedError,
)
from domain.core.singleton_metaclass import Singleton
from domain.models import Post
from domain.repositories import PostRepository


User = get_user_model()


class PostService(metaclass=type(Singleton)):
    @inject
    def __init__(self, repo: PostRepository = PostRepository()):
        super().__init__()
        self.repo = repo

    def get_all(self) -> Optional[QuerySet[Post]]:
        return self.repo.get_all()

    def get_by_id(self, post_id: str) -> Optional[Post]:
        post = self.repo.get_by_id(post_id)
        if not post:
            raise ObjectDoesNotExistError(Post, post_id)
        return post

    def get_by_user(self, user_id: str) -> Optional[QuerySet[Post]]:
        return self.repo.get_by_user(user_id)

    def create(self, actor: User, data: dict) -> Post:
        data['creator'] = actor
        try:
            return self.repo.create(data)
        except IntegrityError:
            raise ValidationError

    def update(self, actor: User, post_id: str, data: dict) -> Optional[Post]:
        post = self.repo.get_by_id(post_id)

        if not post:
            raise ObjectDoesNotExistError(Post, post_id)

        if actor.is_staff or actor == post.creator:
            try:
                return self.repo.update(post, data)
            except IntegrityError:
                raise ValidationError
        else:
            raise UserNotAuthorizedError

    def delete(self, actor: User, post_id: str) -> Optional[Post]:
        post = self.repo.get_by_id(post_id)
        if not post:
            raise ObjectDoesNotExistError(Post, post_id)

        if actor.is_staff or actor == post.creator:
            deleted_post = self.repo.delete_post(post)
            return deleted_post
        else:
            raise UserNotAuthorizedError
