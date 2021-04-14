from django.views.generic import TemplateView

from dark.models.tournament.team import Team
from dark.models.tournament.team import TeamBot
from dark.models.tournament import TournamentRound


class AllTeamBotsView(TemplateView):
    template_name = 'dark/tournament/team/bot/all.html'

    def get_context_data(self, **kwargs):
        team = Team.objects.get(id=self.kwargs['team'])
        rounds = TournamentRound.objects.filter(tournament=team.tournament)
        round_bot_pairs = []
        for tround in rounds:
            try:
                bot = TeamBot.objects.get(tround=tround)
            except TeamBot.DoesNotExist:
                bot = None
            round_bot_pairs.append((tround, bot))
        context = super(AllTeamBotsView, self).get_context_data(**kwargs)
        context.update({
            'team': team,
            'round_bot_pairs': round_bot_pairs
        })
        return context
