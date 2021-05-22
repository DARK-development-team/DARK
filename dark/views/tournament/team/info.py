from django.utils import timezone
from django.views.generic import DetailView

from dark.common.views import UserAuthenticationDependentContextMixin
from dark.models.tournament.team import Team, TeamMember, TeamBot
from dark.models.tournament import TournamentRound, Tournament


class TeamInfoView(UserAuthenticationDependentContextMixin, DetailView):
    model = Team
    template_name = 'dark/tournament/team/info.html'
    context_object_name = 'team'
    slug_url_kwarg = 'team'
    slug_field = 'id'

    def get_common_context(self):
        tournament = Tournament.objects.get(pk=self.object.tournament.pk)
        rounds = TournamentRound.objects.filter(tournament=tournament)
        round_bot_editable_trios = []
        now = timezone.now()
        for tround in rounds:
            try:
                bot = TeamBot.objects.get(tround=tround, team=self.object)
            except TeamBot.DoesNotExist:
                bot = None
            editable = True if tround.start_date > now else False
            round_bot_editable_trios.append((tround, bot, editable))
        return {
            'members': TeamMember.objects.filter(team=self.object),
            'round_bot_editable_trios': round_bot_editable_trios,
            'tournament_editable': True if tournament.start_date > now else False
        }

    def get_authenticated_context_data(self, **kwargs):
        common = self.get_common_context()
        try:
            common.update({
                'user_member': TeamMember.objects
                    .filter(team=self.object)
                    .get(user=self.request.user)
            })
            return common
        except:
            return common

    def get_not_authenticated_context_data(self, **kwargs):
        return self.get_common_context()
