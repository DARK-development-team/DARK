from django.views.generic import DeleteView
from django.urls import reverse

from dark.models.tournament.team import TeamRole
from dark.views.tournament.mixins import TournamentEditableMixin


class RemoveTeamRoleView(TournamentEditableMixin, DeleteView):
    model = TeamRole
    template_name = 'dark/tournament/team/role/remove.html'
    context_object_name = 'role'
    slug_url_kwarg = 'role'
    slug_field = 'id'

    def get_success_url(self):
        return reverse('tournament:team:role:all', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id,
        })
