from django.db import models

from core.models import AuditableModel

# Create your models here.
from users.models import User


class Content(AuditableModel):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contents')

    def __str__(self):
        return f'{self.id} - {self.title[:20]}'
