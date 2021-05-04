import builtins
import os
import uuid

from django.db import models
from django.dispatch import receiver

from .. import Team
from dark.models.tournament import TournamentRound


bot_code_base_store_directory = "dark/data"


def bot_code_upload_path(instance, filename):
    return f'{bot_code_base_store_directory}/bots/' \
           f'{instance.team.tournament.name}{{{instance.team.tournament.id}}}/' \
           f'{str(uuid.uuid4())}.py'


class TeamBot(models.Model):

    max_length = 65535

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tround = models.ForeignKey(TournamentRound, on_delete=models.CASCADE)
    bot_code = models.FileField(default=None, max_length=max_length, upload_to=bot_code_upload_path)

    def __str__(self):
        return self.bot_code.name

    class Meta:
        ordering = ['team', 'tround']
        unique_together = ("team", "tround")


@receiver(models.signals.post_delete, sender=TeamBot)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.bot_code:
        if os.path.isfile(instance.bot_code.path):
            os.remove(instance.bot_code.path)


@receiver(models.signals.pre_save, sender=TeamBot)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.id:
        return False

    try:
        old_file = TeamBot.objects.get(id=instance.id).bot_code
    except TeamBot.DoesNotExist:
        return False

    new_file = instance.bot_code
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


def secure_importer(name, **kwargs):
    # need some import wrapper that allows only basic python
    # functionality + gupb modules
    module = builtins.__import__(name, **kwargs)
    return module


@receiver(models.signals.post_save, sender=TeamBot)
def run_sandbox_check_correct_code(sender, instance, **kwargs):
    file = TeamBot.objects.get(id=instance.id).bot_code

    with open(file.path, 'r') as code:
        file_content = code.read()
        obj = compile("print('hello')", '', 'exec')
        globs = {
            '__builtins__': {
                '__import__': secure_importer,
            }
        }
        # TODO: sandboxing should be done here and if program failed to execute (or just parse)
        # then throw some error and which would indicate that invalid program has been supplied
        # TODO: bot must be executed in context (i.e importable modules) of platform
        # and should be allowed to import basic (safe) builtin python modules
        # maybe find some python sandboxing tool
        # exec(obj, globs)


