import os
from dark.logic.platform_utils import\
    clone_platform, \
    remove_platform, \
    update_platform_url, \
    update_platform_commit,\
    update_platform_name\
from dark.logic.platform_model_logic import is_repository


from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db import IntegrityError


class Platform(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    url = models.URLField(blank=False)
    commit = models.CharField(max_length=50)
    package_to_run = models.CharField(max_length=30)
    platform_relative_wd = models.CharField(max_length=30, default='.')

    default_extra_config = models.JSONField(default='{}')
    customizable_extra_config_fields = models.JSONField(default='{}')
    customizable_extra_config_fields_values = models.JSONField(default='{}')

    class Meta:
        unique_together = ('url', 'commit')

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Platform)
def remove_platform_on_delete(sender, instance: Platform, **kwargs):
    remove_platform(instance.name)


@receiver(pre_save, sender=Platform)
def clone_or_update_platform_on_save(sender, instance: Platform, **kwargs):
    if not is_repository(instance.url):
        raise IntegrityError()

    updated_object = None
    try:
        updated_object = Platform.objects.get(id=instance.id)
        is_update = True
    except Platform.DoesNotExist:
        is_update = False
    else:
        is_update = False

    if is_update:
        commit_updated = False

        update_name = updated_object.name != instance.name
        update_url = updated_object.url != instance.url
        update_commit = updated_object.commit != instance.commit

        if update_name and update_url:
            remove_platform(instance.name)
            clone_platform(instance.name, instance.url, instance.commit)
            commit_updated = True
        elif update_name:
            update_platform_name(updated_object.name, instance.name)
            commit_updated = True
        elif update_url:
            update_platform_url(instance.name, instance.url, instance.commit)
            commit_updated = True

        if update_commit and not commit_updated:
            update_platform_commit(instance.name, instance.commit)
    else:
        clone_platform(instance.name, instance.url, instance.commit)
