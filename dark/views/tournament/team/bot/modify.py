from django.contrib import messages
from django.db import IntegrityError
from django.views.generic import UpdateView
from django.urls import reverse

from dark.models.tournament.team import TeamBot
from dark.forms.tournament.team import ModifyTeamBotForm
from dark.views.tournament.tround.mixins import RoundEditableMixin


class ModifyTeamBotView(RoundEditableMixin, UpdateView):
    model = TeamBot
    form_class = ModifyTeamBotForm
    template_name = 'dark/tournament/team/bot/modify.html'
    context_object_name = 'bot'
    slug_url_kwarg = 'bot'
    slug_field = 'id'

    def form_valid(self, form):
        try:
            messages.success(self.request, 'Bot ' + form.cleaned_data.get('bot_symbol_name') + 'has been successfully '
                                                                                              'modified!')
            return super(ModifyTeamBotView, self).form_valid(form)
        except IntegrityError as e:
            messages.error(self.request, f'Failed to modify bot - make sure that field values are valid')
            return super(ModifyTeamBotView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('tournament:team:info', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id
        })
