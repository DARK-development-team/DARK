from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.urls import reverse

from dark.models.tournament import Tournament, TournamentRound
from dark.models.tournament.team import TeamBot, Team
from dark.forms.tournament.team import AddTeamBotForm
from dark.common.views import ForeignKeysMixin

class AddTeamBotView(View):
    form_class = AddTeamBotForm
    template_name = 'dark/tournament/team/bot/add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, tournament, team, tround,  *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form.instance.team = Team.objects.get(id=team)
        form.instance.tround = TournamentRound.objects.get(id=tround)
        if "cancel" in request.POST:
            return redirect(reverse('tournament:team:info', kwargs={
                'tournament': tournament,
                'team': team
            }))
        if form.is_valid():
            obj = form.save()
            return redirect(reverse('tournament:team:info', kwargs={
                'tournament': obj.team.tournament.id,
                'team': obj.team.id
            }))
        else:
            return render(request, self.template_name, {'form': form})


