import django.db
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse

from dark.models.tournament import Tournament
from dark.forms.tournament import AddTournamentForm
from dark.models.tournament.team import Team, TeamRole


class AddTournamentView(CreateView):
    model = Tournament
    template_name = 'dark/tournament/add.html'
    form_class = AddTournamentForm

    def form_valid(self, form):
        creator = self.request.user

        try:
            self.object = form.save(commit=False)
            self.object.creator = creator
            self.object.save()

            tournament = Tournament.objects.get(pk=self.object.id)

            tournament.participants.add(creator)

            number_of_teams = form.cleaned_data.get('number_of_teams')

            for i in range(number_of_teams):
                team_name = 'Team ' + str(i + 1)
                team = Team.objects.create(tournament_id=self.object.id, name=team_name)
                TeamRole.objects.create(team=team, name="Participant")

            return redirect(self.get_success_url())
        except IntegrityError as e:
            messages.error(self.request, f'Failed to add tournament - make sure that field values are valid')
            return super(AddTournamentView, self).form_invalid(form)



    def get_success_url(self):
        return reverse('tournament:info', kwargs={
            'tournament': self.object.id
        })
