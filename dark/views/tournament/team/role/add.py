from django.views.generic import CreateView
from django.urls import reverse

from dark.models.tournament.team import Team
from dark.forms.tournament.team import AddTeamRoleForm
from dark.common.views import ForeignKeysMixin


class AddTeamRoleView(ForeignKeysMixin, CreateView):
    model = Team
    template_name = 'dark/tournament/team/role/add.html'
    form_class = AddTeamRoleForm
    url_kwargs = ['team']
    url_kwarg_fields = ['team']

    def get_success_url(self):
        return reverse('tournament:team:role:all', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id,
        })
