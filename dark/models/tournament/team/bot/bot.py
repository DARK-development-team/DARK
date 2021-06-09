import builtins
import os
import uuid

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from dark.common.git import remove_git_repo
from dark.common.models.fields import GitRepoField
from .. import Team
from dark.models.tournament import TournamentRound


bot_code_base_store_directory = "dark/data"


def bot_code_upload_path(instance):
    return f'{bot_code_base_store_directory}/bots/' \
           f'{instance.team.tournament.name}{{{instance.team.tournament.id}}}/' \
           f'{str(uuid.uuid4())}/'


class TeamBot(models.Model):

    max_length = 65535

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tround = models.ForeignKey(TournamentRound, on_delete=models.CASCADE)

    bot = GitRepoField(local_directory=bot_code_upload_path, unique=True)
    bot_package = models.CharField(max_length=30)
    bot_package_relative_wd = models.CharField(max_length=30)
    bot_symbol_name = models.CharField(default=None, max_length=30)

    def __str__(self):
        return self.bot_symbol_name

    class Meta:
        ordering = ['team', 'tround']
        unique_together = ("team", "tround")


@receiver(post_delete, sender=TeamBot)
def remove_platform_on_delete(sender, instance: TeamBot, **kwargs):
    remove_git_repo(instance.bot.local_directory)
