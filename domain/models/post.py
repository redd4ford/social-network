from django.contrib.auth import get_user_model
from django.db import models

from domain.core.models import BasePKModel

User = get_user_model()


class Post(BasePKModel):
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=True)
    creator = models.ForeignKey(
        User,
        related_name='posts',
        blank=False,
        on_delete=models.CASCADE
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked',
        through='domain.Like',
        blank=True,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
