from django.db import models

from .. import Team
from dark.models.user import User
from .. import TeamRole


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(TeamRole, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ("team", "user")
        ordering = ['team', 'user']
