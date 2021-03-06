from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import View

from dark.models.tournament.team import Team, TeamRole, TeamMember
from dark.views.tournament.mixins import TournamentEditableMixin


class JoinTeamMemberView(TournamentEditableMixin, View):
    def get(self, request, tournament, team):
        try:
            team_obj = Team.objects.get(id=team)
            user = request.user
            role = TeamRole.objects.get(team=team_obj, name="Participant")

            TeamMember.objects.create(team=team_obj, user=user, role=role)
            messages.success(request, 'You have joined ' + team_obj.name)

            return HttpResponseRedirect(
                reverse('tournament:team:info', kwargs={'tournament': tournament, 'team': team}))
        except IntegrityError as e:
            messages.error(self.request, f'Failed to join team')
            return HttpResponseRedirect(
                reverse('tournament:info', kwargs={'tournament': tournament}))

