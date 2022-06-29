# Create your models here.
import uuid

from django.db import models


class BaseMeta(object):
    ordering = ("-created_at",)


class BaseModel(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, db_index=True
    )
    changed_at = models.DateTimeField(
        auto_now=True, editable=False, db_index=True
    )

    class Meta:
        abstract = True
