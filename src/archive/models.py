from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


class SavingManager(models.Manager):
    def total_quantity(self):
        return self.aggregate(
            total_quantity=Coalesce(Sum("tree_quantity"), 0)
        ).get("total_quantity")


class Saving(models.Model):
    name = models.CharField(max_length=100)
    tree_quantity = models.PositiveIntegerField()
    objects = SavingManager()
