from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView

from dark.common.decorators import after
from dark.common.views import ForeignKeysMixin, TournamentEditableMixin
from dark.forms.tournament.team import AddTeamForm
from dark.models.tournament.team import Team, TeamRole, TeamMember


class AddTeamView(LoginRequiredMixin, ForeignKeysMixin, TournamentEditableMixin, CreateView):
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

    def add_members(self, form):
        team = self.object
        TeamRole.objects.create(team=team, name="Organizer", can_modify_members=True, can_remove=True)
        participant_role = TeamRole.objects.create(team=team, name="Participant")

        TeamMember.objects.create(team=team, user=self.request.user, role=participant_role)

    @after(add_members)
    def form_valid(self, form):
        return super(AddTeamView, self).form_valid(form)
