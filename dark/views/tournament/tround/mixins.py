from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from dark.models.tournament import Tournament, TournamentRound
from dark.models.tournament.team import TeamBot


class RoundAddableMixin(object):
    def dispatch(self, request, *args, **kwargs):
        tournament = get_object_or_404(Tournament, id=self.kwargs['tournament'])
        now = timezone.now()

        if now < tournament.end_date:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'Tournament is no longer editable!')
            return redirect(reverse('tournament:info', kwargs={'tournament': self.kwargs['tournament']}))


class RoundEditableMixin(object):
    def dispatch(self, request, *args, **kwargs):
        now = timezone.now()

        if 'tround' in kwargs:
            tround = get_object_or_404(TournamentRound, id=self.kwargs['tround'])
        else:
            bot = get_object_or_404(TeamBot, id=self.kwargs['bot'])
            tround = bot.tround

        if tround.start_date > now:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'Round is no longer editable!')
            return redirect(reverse('tournament:team:info',
                                    kwargs={'tournament': self.kwargs['tournament'], 'team': self.kwargs['team']}))
