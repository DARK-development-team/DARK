from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView

from dark.models.tournament import Tournament
from dark.models.tournament import TournamentRound
from dark.models.tournament.team import Team


class TournamentInfoView(DetailView):
    model = Tournament
    template_name = 'dark/tournament/info.html'
    context_object_name = 'tournament'
    slug_url_kwarg = 'tournament'
    slug_field = 'id'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('tournament:all'))

        try:
            self.object = self.get_object()
        except Http404:
            return redirect(reverse('tournament:all'))

        tournament = self.object
        user = request.user

        if tournament.is_private and user not in tournament.participants.all():
            return redirect(reverse('tournament:all'))

        context = super().get_context_data(object=tournament)
        context['rounds'] = TournamentRound.objects.filter(tournament=tournament)
        context['contestants'] = Team.objects.filter(tournament=tournament)
        context['is_creator_viewing'] = tournament.creator == user
        context['is_private'] = tournament.is_private
        context['has_team'] = True if Tournament.objects.filter(team__teammember__user=user).filter(
            id=tournament.id).count() != 0 else False

        return self.render_to_response(context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rounds'] = TournamentRound.objects.filter(tournament=self.object)
    #     context['contestants'] = Team.objects.filter(tournament=self.object)
    #     context['is_creator_viewing'] = self.object.creator == self.request.user
    #     context['is_private'] = self.object.is_private
    #     context['has_team'] = True if Tournament.objects.filter(team__teammember__user=self.request.user).filter(
    #         id=self.object.id).count() != 0 else False
    #     return context
