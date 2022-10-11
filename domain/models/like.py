from django.contrib.auth import get_user_model
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from domain.core.models import BasePKModel
from domain.models import Post

User = get_user_model()


class Like(ExportModelOperationsMixin('like'), BasePKModel):
    updated_at = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    class Meta:
        unique_together = ('user', 'post',)
