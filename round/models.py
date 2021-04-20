from django.db import models

from tournament.models import Tournament


class Round(models.Model):
    name = models.CharField(max_length=30, blank=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name
