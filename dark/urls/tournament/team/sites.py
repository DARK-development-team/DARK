from django.urls import path

from dark.views.tournament.team import AllTeamsView, AddTeamView, TeamInfoView, ChangeTeamNameView, RemoveTeamView
from dark.views.tournament.team.member import JoinTeamMemberView
from . import bot
from . import member
from . import role


class TeamSite:
    def get_urls(self):
        urlpatterns = [
            path('all', AllTeamsView.as_view(),  name='all'),
            path('add', AddTeamView.as_view(), name='add'),
            path('<int:team>/join', JoinTeamMemberView.as_view(), name='join'),
            path('<int:team>', TeamInfoView.as_view(), name='info'),
            path('<int:team>/remove', RemoveTeamView.as_view(), name='remove'),
            path('<int:team>/change_name', ChangeTeamNameView.as_view(), name='change name'),
            path('<int:team>/roles/', role.site.urls),
            path('<int:team>/members/', member.site.urls),
            path('<int:team>/bots/', bot.site.urls),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'team', 'team'


site = TeamSite()
