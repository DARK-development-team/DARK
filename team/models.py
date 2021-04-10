from django.db import models as dmodels
from tournament.models import Tournament
from users.models import User

class Team(dmodels.Model):
    tournament_ID = dmodels.ForeignKey(Tournament, on_delete=dmodels.CASCADE)
    name = dmodels.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['tournament_ID', 'id']

class TeamRole(dmodels.Model):
    team_ID = dmodels.ForeignKey(Team, on_delete=dmodels.CASCADE)
    name = dmodels.CharField(max_length=30)
    can_modify_members = dmodels.BooleanField(default=False)
    can_remove = dmodels.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("team_ID", "name")

class TeamMember(dmodels.Model):
    team_ID = dmodels.ForeignKey(Team, on_delete=dmodels.CASCADE)
    user_ID = dmodels.ForeignKey(User, on_delete=dmodels.CASCADE)
    role_ID = dmodels.ForeignKey(TeamRole, on_delete=dmodels.CASCADE)

    def __str__(self):
        return str(self.user_ID)

    class Meta:
        unique_together = ("team_ID", "user_ID")
        ordering = ['team_ID', 'user_ID']