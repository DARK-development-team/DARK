from django.db import models as dmodels
from tournament.models import Tournament
from users.models import User


class Team(dmodels.Model):
    tournament = dmodels.ForeignKey(Tournament, on_delete=dmodels.CASCADE)
    name = dmodels.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['tournament', 'id']


class TeamRole(dmodels.Model):
    team = dmodels.ForeignKey(Team, on_delete=dmodels.CASCADE)
    name = dmodels.CharField(max_length=30)
    can_modify_members = dmodels.BooleanField(default=False)
    can_remove = dmodels.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("team", "name")


class TeamMember(dmodels.Model):
    team = dmodels.ForeignKey(Team, on_delete=dmodels.CASCADE)
    user = dmodels.ForeignKey(User, on_delete=dmodels.CASCADE)
    role = dmodels.ForeignKey(TeamRole, on_delete=dmodels.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ("team", "user")
        ordering = ['team', 'user']
