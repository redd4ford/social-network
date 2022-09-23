import uuid

from django.db import models


class BasePKModel(models.Model):
    """ Base model with UUID and created_at/updated_at fields. """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def get_verbose(self):
        return self._meta.verbose_name.title()
