from django.views.generic import DeleteView
from django.urls import reverse

from dark.common.views import TournamentEditableMixin
from dark.models.tournament.team import Team


class RemoveTeamView(TournamentEditableMixin, DeleteView):
    model = Team
    template_name = 'dark/tournament/team/remove.html'
    context_object_name = 'team'
    slug_url_kwarg = 'team'
    slug_field = 'id'

    def get_success_url(self):
        return reverse('tournament:info', kwargs={
            'tournament': self.object.tournament.id
        })
