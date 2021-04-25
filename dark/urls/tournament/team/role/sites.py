from django.urls import path

from dark.views.tournament.team.role import AllTeamRolesView, AddTeamRoleView, ModifyTeamRoleView, RemoveTeamRoleView


class TeamRoleSite:
    def get_urls(self):
        urlpatterns = [
            path('all', AllTeamRolesView.as_view(), name='all'),
            path('add', AddTeamRoleView.as_view(), name='add'),
            path('<int:role>/modify', ModifyTeamRoleView.as_view(), name='modify'),
            path('<int:role>/remove', RemoveTeamRoleView.as_view(), name='remove'),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'role', 'role'


site = TeamRoleSite()
