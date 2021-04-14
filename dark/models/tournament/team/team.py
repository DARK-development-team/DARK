from django.db import models

from dark.models.tournament import Tournament


class Team(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['tournament', 'id']
        unique_together = ('tournament', 'name')
