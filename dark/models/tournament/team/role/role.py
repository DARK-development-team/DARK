from django.db import models

from .. import Team


class TeamRole(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    can_modify_members = models.BooleanField(default=False)
    can_remove = models.BooleanField(default=False)

    def __str__(self):
        return self.name
