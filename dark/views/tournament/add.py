from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse

from dark.models.tournament import Tournament
from dark.forms.tournament import AddTournamentForm
from dark.models.tournament.team import Team


class AddTournamentView(CreateView):
    model = Tournament
    template_name = 'dark/tournament/add.html'
    form_class = AddTournamentForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()

        number_of_teams = form.cleaned_data.get('number_of_teams')

        for i in range(number_of_teams):
            team_name = 'Team ' + str(i + 1)
            team = Team(tournament_id=self.object.id, name=team_name)
            team.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('tournament:info', kwargs={
            'tournament': self.object.id
        })
