from django.views.generic import ListView

from dark.models.tournament.team import Team
from dark.models.tournament.team import TeamRole


class AllTeamRolesView(ListView):
    model = TeamRole
    template_name = 'dark/tournament/team/role/all.html'
    context_object_name = 'roles'

    def get_queryset(self):
        team = Team.objects.get(id=self.kwargs['team'])
        self.team = team
        return TeamRole.objects.filter(team=team)

    def get_context_data(self, **kwargs):
        context = super(AllTeamRolesView, self).get_context_data(**kwargs)
        context.update({
            'team': self.team
        })
        return context
