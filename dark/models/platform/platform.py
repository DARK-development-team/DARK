import os
from dark.logic.platform_utils import full_platform_path, pull_platform, reload_platform, remove_platform

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import IntegrityError


class Platform(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    address = models.URLField(blank=False)
    commit = models.CharField(max_length=50)
    package_to_run = models.CharField(max_length=30)

    class Meta:
        unique_together = ('address', 'commit')

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Platform)
def auto_delete_platform_on_delete(sender, instance: Platform, **kwargs):
    if os.path.isdir(full_platform_path(instance.name)):
        remove_platform(instance.name)


@receiver(models.signals.pre_save, sender=Platform)
def auto_create_platform_on_save(sender, instance: Platform, **kwargs):
    pull_platform(instance.name, instance.address, instance.commit)
