from django.db import models

from .. import Team
from dark.models.tournament import TournamentRound


class TeamBot(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tround = models.ForeignKey(TournamentRound, on_delete=models.CASCADE)
    bot_url = models.URLField(default=None, blank=True, null=True)

    download_directory = "DARK/bots"

    def __str__(self):
        return self.bot_url

    class Meta:
        ordering = ['team', 'tround']
        unique_together = ("team", "tround")


'''
    def extract_name_from_repo_path(self, repo_path : str):
        full_path = git.Repo(self.bot_url).remotes.origin.url
        repo_name = full_path.split('.git')[0].split('/')[-1]
        return repo_name

    def sync(self):
        git.Git(f'{Bot.download_directory}/'
                f'{self.team.name}/'
                f'{self.tround.name}/'
                f'{self.extract_name_from_repo_path(self.bot_url)}')\
            .clone(self.bot_url)

    def run_on(self, tround: Round):
        self.sync()
        pass
'''
