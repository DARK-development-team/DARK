from django.views.generic import UpdateView
from django.urls import reverse

from dark.models.tournament.team import TeamRole
from dark.forms.tournament.team import ModifyTeamRoleForm
from dark.views.tournament.mixins import TournamentEditableMixin


class ModifyTeamRoleView(TournamentEditableMixin, UpdateView):
    model = TeamRole
    form_class = ModifyTeamRoleForm
    template_name = 'dark/tournament/team/role/modify.html'
    context_object_name = 'role'
    slug_url_kwarg = 'role'
    slug_field = 'id'

    def get_success_url(self):
        return reverse('tournament:team:role:all', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id
        })
