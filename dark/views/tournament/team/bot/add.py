from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View

from dark.forms.tournament.team import AddTeamBotForm
from dark.models.tournament import TournamentRound
from dark.models.tournament.team import Team
from dark.views.tournament.tround.mixins import RoundEditableMixin


class AddTeamBotView(RoundEditableMixin, View):
    form_class = AddTeamBotForm
    template_name = 'dark/tournament/team/bot/add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, tournament, team, tround, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form.instance.team = Team.objects.get(id=team)
        form.instance.tround = TournamentRound.objects.get(id=tround)
        if "cancel" in request.POST:
            return redirect(reverse('tournament:team:info', kwargs={
                'tournament': tournament,
                'team': team
            }))
        if form.is_valid():
            try:
                obj = form.save()
                messages.success(request, 'Bot ' + obj.bot_symbol_name + ' has successfully added!')
                return redirect(reverse('tournament:team:info', kwargs={
                    'tournament': obj.team.tournament.id,
                    'team': obj.team.id
                }))
            except IntegrityError as e:
                messages.error(self.request, f'Failed to add bot - make sure that field values are valid')
                return render(request, self.template_name, {'form': form})

        else:
            return render(request, self.template_name, {'form': form})
