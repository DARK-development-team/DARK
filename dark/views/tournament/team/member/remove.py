from django.views.generic import DeleteView
from django.urls import reverse

from dark.models.tournament.team import TeamMember
from dark.views.tournament.mixins import TournamentEditableMixin


class RemoveTeamMemberView(TournamentEditableMixin, DeleteView):
    model = TeamMember
    template_name = 'dark/tournament/team/member/remove.html'
    context_object_name = 'member'
    slug_url_kwarg = 'member'
    slug_field = 'id'

    def get_success_url(self):
        return reverse('tournament:team:info', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id,
        })
