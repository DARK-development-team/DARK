from django.db import models as dmodels
from team.models import Team
from round.models import Round


class Bot(dmodels.Model):
    team = dmodels.ForeignKey(Team, on_delete=dmodels.CASCADE)
    round = dmodels.ForeignKey(Round, on_delete=dmodels.CASCADE)
    bot_url = dmodels.URLField(default=None, blank=True, null=True)

    download_directory = "DARK/bots"

    def __str__(self):
        return self.bot_url

    class Meta:
        ordering = ['team', 'round']
        unique_together = ("team", "round")
