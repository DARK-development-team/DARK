import os

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
    # extra_config_values = models.JSONField(default=dict)

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
