from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin

from dark.common.views import UserAuthenticationDependentContextMixin
from dark.models.tournament.team import Team


class AllTeamsView(UserAuthenticationDependentContextMixin, SingleObjectMixin, TemplateView):
    template_name = 'dark/tournament/team/all.html'
    context_object_name = 'tournament'
    slug_url_kwarg = 'tournament'
    slug_field = 'id'

    def get_authenticated_context_data(self, **kwargs):
        return {
            'teams': Team.objects
                .filter(tournament=self.get_object()),
            'your_team': Team.objects
                .filter(tournament=self.get_object())
                .get(teammember__user=self.request.user)
        }

    def get_not_authenticated_context_data(self, **kwargs):
        return {
            'teams': Team.objects
                .filter(tournament=self.get_object())
        }
