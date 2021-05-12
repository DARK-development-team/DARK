from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from dark.models.tournament import TournamentRound
from dark.logic import tround_utils


class TournamentRoundInfoView(DetailView):
    model = TournamentRound
    template_name = 'dark/tournament/tround/info.html'
    context_object_name = 'tround'
    slug_url_kwarg = 'tround'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round = get_object_or_404(TournamentRound, id=self.kwargs['tround'])
        #tround_utils.execute_round()
        #context['results'] = tround_utils.get_round_results()
        context['is_creator_viewing'] = True if round.tournament.creator == self.request.user else False
        return context
