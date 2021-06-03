from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse

from dark.models.tournament.team import Team, TeamRole, TeamMember
from dark.forms.tournament.team import AddTeamForm
from dark.common.views import ForeignKeysMixin


class AddTeamView(LoginRequiredMixin, ForeignKeysMixin, CreateView):
    model = Team
    template_name = 'dark/tournament/team/add.html'
    form_class = AddTeamForm
    url_kwargs = ['tournament']
    url_kwarg_fields = ['tournament']

    def get_success_url(self):
        return reverse('tournament:team:info', kwargs={
            'tournament': self.object.tournament.id,
            'team': self.object.id
        })

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            tournament_id = kwargs.get('tournament')
            return redirect(reverse('tournament:info', kwargs={
                'tournament': tournament_id
            }))
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            team = self.object
            TeamRole.objects.create(team=team, name="Organizer", can_modify_members=True, can_remove=True)
            participant_role = TeamRole.objects.create(team=team, name="Participant")

            TeamMember.objects.create(team=team, user=self.request.user, role=participant_role)

            return super(AddTeamView, self).form_valid(form)
        except IntegrityError as e:
            messages.error(self.request, f'Failed to add team - make sure that field values are valid')
            return super(AddTeamView, self).form_invalid(form)

