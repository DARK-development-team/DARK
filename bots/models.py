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


'''
    def extract_name_from_repo_path(self, repo_path : str):
        full_path = git.Repo(self.bot_url).remotes.origin.url
        repo_name = full_path.split('.git')[0].split('/')[-1]
        return repo_name
        
    def sync(self):
        git.Git(f'{Bot.download_directory}/'
                f'{self.team.name}/'
                f'{self.round.name}/'
                f'{self.extract_name_from_repo_path(self.bot_url)}')\
            .clone(self.bot_url)

    def run_on(self, round: Round):
        self.sync()
        pass
'''
