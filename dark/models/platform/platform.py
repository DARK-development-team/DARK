from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import IntegrityError


class Platform(models.Model):
    name = models.CharField(max_length=30, blank=False)
    address = models.URLField(blank=False, unique=False)
    commit = models.CharField(max_length=50)
    package_to_run = models.CharField(max_length=30)

    class Meta:
        unique_together = ('address', 'commit')

    def __str__(self):
        return self.name
