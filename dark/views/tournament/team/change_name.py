from django.views.generic import UpdateView
from django.urls import reverse

from dark.models.tournament.team import Team
from dark.forms.tournament.team import ChangeTeamNameForm


class ChangeTeamNameView(UpdateView):
    model = Team
    form_class = ChangeTeamNameForm
    template_name = 'dark/tournament/team/change_name.html'
    slug_url_kwarg = 'team'
    slug_field = 'id'

    def get_success_url(self):
        return reverse('tournament:team:info', kwargs={
            'tournament': self.object.tournament.id,
            'team': self.object.id
        })
