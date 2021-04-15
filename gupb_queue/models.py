from django.db import models

from tournament.models import Tournament
from platforms.models import Platform

class Queue(models.Model):
    name = models.CharField(max_length=30, blank=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
