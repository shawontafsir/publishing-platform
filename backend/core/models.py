from django.db import models

# Create your models here.
from model_utils.managers import SoftDeletableManager
from model_utils.models import TimeStampedModel, SoftDeletableModel


class AuditableModel(TimeStampedModel, SoftDeletableModel):
    objects = models.Manager()
    soft_manager = SoftDeletableManager()

    class Meta:
        abstract = True
