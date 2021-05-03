import os
from dark.logic.tround_utils import full_tround_path, create_tround, prepare_tround_venv, reload_tround, remove_tround

from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db import IntegrityError

from dark.models.platform.platform import Platform
from .. import Tournament


class TournamentRound(models.Model):
    name = models.CharField(max_length=30, blank=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('tournament', 'name')
        constraints = [
            models.CheckConstraint(check=models.Q(start_date__lt=models.F("end_date")),
                                   name='round_start_date_lt_end_date'),
        ]


@receiver(pre_save, sender=TournamentRound)
def start_date_ge_tournament_start_date(sender, **kwargs):
    instance: TournamentRound = kwargs['instance']
    if instance.start_date < instance.tournament.start_date:
        raise IntegrityError()


@receiver(pre_save, sender=TournamentRound)
def end_date_le_tournament_end_date(sender, **kwargs):
    instance: TournamentRound = kwargs['instance']
    if instance.end_date > instance.tournament.end_date:
        raise IntegrityError()


@receiver(post_delete, sender=TournamentRound)
def auto_delete_tround_on_delete(sender, instance: TournamentRound, **kwargs):
    if os.path.isdir(full_tround_path(instance.name, instance.tournament)):
        remove_tround(instance.name, instance.tournament)


@receiver(pre_save, sender=TournamentRound)
def auto_create_tround_on_save(sender, instance: TournamentRound, **kwargs):
    create_tround(instance.name, instance.tournament, instance.platform)
    prepare_tround_venv(instance.name, instance.tournament)
