from django.views.generic import DeleteView
from django.urls import reverse

from dark.models.tournament.team import TeamBot


class RemoveTeamBotView(DeleteView):
    model = TeamBot
    template_name = 'dark/tournament/team/bot/remove.html'
    context_object_name = 'bot'
    slug_url_kwarg = 'bot'
    slug_field = 'id'

    def get_success_url(self):
        return reverse('tournament:team:bot:all', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id,
        })
