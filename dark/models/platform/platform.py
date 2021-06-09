import shutil
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from dark.common.models.fields import GitRepoField
from dark.logic.platform_utils import platform_relative_local_directory
from dark.common.git import remove_git_repo

def platform_repo_local_directory_path(instance):
    return platform_relative_local_directory(instance.name)


class Platform(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    repo = GitRepoField(local_directory=platform_repo_local_directory_path, unique=True)
    package_to_run = models.CharField(max_length=30)
    platform_relative_wd = models.CharField(max_length=30, default='.')
    platform_config_relative_path = models.CharField(max_length=30, default='gupb/default_config.py')

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Platform)
def remove_platform_on_delete(sender, instance: Platform, **kwargs):
    remove_git_repo(instance.repo.local_directory)
