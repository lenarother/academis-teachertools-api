import uuid

from django.db import models


class Question(models.Model):
    uuid = models.UUIDField(
        verbose_name='UUID',
        default=uuid.uuid4,
        editable=False,
    )
    body = models.TextField(
        verbose_name='Body',
    )
    created = models.DateTimeField(
        verbose_name='Created',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.body[:20]}...'
