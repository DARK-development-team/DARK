from django.views.generic import DetailView

from dark.models.tournament import Tournament
from dark.models.tournament import TournamentRound
from dark.models.tournament.team import Team


class TournamentInfoView(DetailView):
    model = Tournament
    template_name = 'dark/tournament/info.html'
    context_object_name = 'tournament'
    slug_url_kwarg = 'tournament'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rounds'] = TournamentRound.objects.filter(tournament=self.object)
        context['contestants'] = Team.objects.filter(tournament=self.object)
        context['is_creator_viewing'] = self.object.creator == self.request.user
        return context
