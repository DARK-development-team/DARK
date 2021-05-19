from django.contrib import messages
from django.views.generic import DeleteView
from django.urls import reverse

from dark.common.views import RoundEditableMixin
from dark.models.tournament.team import TeamBot


class RemoveTeamBotView(RoundEditableMixin, DeleteView):
    model = TeamBot
    template_name = 'dark/tournament/team/bot/remove.html'
    context_object_name = 'bot'
    slug_url_kwarg = 'bot'
    slug_field = 'id'

    def delete(self, request, *args, **kwargs):
        get_kwargs = {
            self.slug_field: kwargs[self.slug_url_kwarg]
        }
        bot = TeamBot.objects.get(**get_kwargs)
        messages.success(self.request, 'Bot ' + bot.bot_class_name + ' has successfully deleted!')
        return super(RemoveTeamBotView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('tournament:team:info', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id,
        })
