from django.views.generic import CreateView
from django.urls import reverse

from dark.models.tournament.team import TeamBot
from dark.forms.tournament.team import AddTeamBotForm
from dark.common.views import ForeignKeysMixin


class AddTeamBotView(ForeignKeysMixin, CreateView):
    model = TeamBot
    template_name = 'dark/tournament/team/bot/add.html'
    form_class = AddTeamBotForm
    url_kwargs = ['team', 'tround']
    url_kwarg_fields = ['team', 'tround']

    def get_success_url(self):
        return reverse('tournament:team:bot:all', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id
        })
