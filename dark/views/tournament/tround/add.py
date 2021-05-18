from django.urls import reverse
from django.views.generic import CreateView

from dark.common.views import ForeignKeysMixin, RoundAddableMixin
from dark.forms.tournament import AddTournamentRoundForm
from dark.models.tournament import TournamentRound


class AddTournamentRoundView(RoundAddableMixin, ForeignKeysMixin, CreateView):
    model = TournamentRound
    template_name = 'dark/tournament/tround/add.html'
    form_class = AddTournamentRoundForm
    url_kwargs = ['tournament']
    url_kwarg_fields = ['tournament']

    def get_success_url(self):
        return reverse('tournament:tround:info', kwargs={
            'tournament': self.object.tournament.id,
            'tround': self.object.id
        })
