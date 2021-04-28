from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView

from dark.common.views import UserAuthenticationDependentContextMixin
from dark.models.tournament import Tournament
from dark.models.tournament import TournamentRound
from dark.models.tournament.team import Team


class TournamentInfoView(UserAuthenticationDependentContextMixin, DetailView):
    model = Tournament
    template_name = 'dark/tournament/info.html'
    context_object_name = 'tournament'
    slug_url_kwarg = 'tournament'
    slug_field = 'id'

    def get(self, request, *args, **kwargs):
        tournament = get_object_or_404(Tournament, id=self.kwargs['tournament'])

        if tournament.is_private:
            if request.user.is_authenticated:
                if request.user not in tournament.participants.all():
                    messages.info(request, 'Tournament is private, enter access key')
                    return redirect(reverse('tournament:access', kwargs={'tournament': self.kwargs['tournament']}))
            else:
                messages.error(request, 'Tournament is private, login first')
                return redirect(reverse('user:login'))

        return super().get(request, *args, **kwargs)

    def get_common_context(self):
        tournament = get_object_or_404(Tournament, id=self.kwargs['tournament'])

        return {
            'rounds': TournamentRound.objects.filter(tournament=tournament),
            'contestants': Team.objects.filter(tournament=tournament),
            'is_creator_viewing': False,
            'is_private': tournament.is_private,
            'has_team': False,
        }

    def get_authenticated_context_data(self, **kwargs):
        tournament = get_object_or_404(Tournament, id=self.kwargs['tournament'])

        context = self.get_common_context()
        context.update({
            'is_creator_viewing': tournament.creator == self.request.user,
            'has_team': True if Tournament.objects.filter(team__teammember__user=self.request.user).filter(
                id=tournament.id).count() != 0 else False
        })
        return context

    def get_not_authenticated_context_data(self, **kwargs):
        return self.get_common_context()
