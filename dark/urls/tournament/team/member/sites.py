from django.urls import path

from dark.views.tournament.team.member import AddTeamMemberView
from dark.views.tournament.team.member import RemoveTeamMemberView
from dark.views.tournament.team.member import TeamMemberInfoView
from dark.views.tournament.team.member import ChangeTeamMemberRoleView


class TeamMemberSite:
    def get_urls(self):
        urlpatterns = [
            path('add', AddTeamMemberView.as_view(), name='add'),
            path('<int:member>/remove', RemoveTeamMemberView.as_view(), name='remove'),
            path('<int:member>', TeamMemberInfoView.as_view(), name='info'),
            path('<int:member>/change_role', ChangeTeamMemberRoleView.as_view(), name='change_role')
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'member', 'member'


site = TeamMemberSite()
