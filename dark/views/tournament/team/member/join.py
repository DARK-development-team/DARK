from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import View

from dark.models.tournament.team import Team, TeamRole, TeamMember


class JoinTeamMemberView(View):
    def get(self, request, tournament, team):
        team_obj = Team.objects.get(id=team)
        user = request.user
        role = TeamRole.objects.create(team=team_obj, name="Default", can_modify_members=True, can_remove=True)

        TeamMember.objects.create(team=team_obj, user=user, role=role)
        messages.success(request, f'Member added!')

        return HttpResponseRedirect(reverse('tournament:team:info', kwargs={'tournament': tournament, 'team': team}))
