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
        context['results'] = tround_utils.get_tround_results()
        return context
