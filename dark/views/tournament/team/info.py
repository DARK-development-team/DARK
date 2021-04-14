from django.views.generic import DetailView

from dark.common.views import UserAuthenticationDependentContextMixin
from dark.models.tournament.team import Team, TeamMember


class TeamInfoView(UserAuthenticationDependentContextMixin, DetailView):
    model = Team
    template_name = 'dark/tournament/team/info.html'
    context_object_name = 'team'
    slug_url_kwarg = 'team'
    slug_field = 'id'

    def get_common_context(self):
        return {
            'members': TeamMember.objects.filter(team=self.object)
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
