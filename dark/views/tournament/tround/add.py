from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView
from django.urls import reverse

from dark.models.tournament import TournamentRound, Tournament
from dark.forms.tournament import AddTournamentRoundForm
from dark.common.views import ForeignKeysMixin, TournamentEditableMixin


class AddTournamentRoundView(TournamentEditableMixin, ForeignKeysMixin, CreateView):
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
