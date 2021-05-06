from django.views.generic import UpdateView
from django.urls import reverse

from dark.models.tournament.team import TeamBot
from dark.forms.tournament.team import ModifyTeamBotForm


class ModifyTeamBotView(UpdateView):
    model = TeamBot
    form_class = ModifyTeamBotForm
    template_name = 'dark/tournament/team/bot/modify.html'
    context_object_name = 'bot'
    slug_url_kwarg = 'bot'
    slug_field = 'id'

    def get_success_url(self):
        return reverse('tournament:team:info', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id
        })
