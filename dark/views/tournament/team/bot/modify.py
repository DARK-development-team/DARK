from django.contrib import messages
from django.views.generic import UpdateView
from django.urls import reverse

from dark.common.views import RoundEditableMixin
from dark.models.tournament.team import TeamBot
from dark.forms.tournament.team import ModifyTeamBotForm


class ModifyTeamBotView(RoundEditableMixin, UpdateView):
    model = TeamBot
    form_class = ModifyTeamBotForm
    template_name = 'dark/tournament/team/bot/modify.html'
    context_object_name = 'bot'
    slug_url_kwarg = 'bot'
    slug_field = 'id'

    def form_valid(self, form):
        messages.success(self.request, 'Bot ' + form.cleaned_data.get('bot_class_name') + ' has successfully modified!')
        return super(ModifyTeamBotView, self).form_valid(form)

    def get_success_url(self):
        return reverse('tournament:team:info', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id
        })
