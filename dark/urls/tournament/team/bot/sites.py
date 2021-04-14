from django.urls import path

from dark.views.tournament.team.bot import AllTeamBotsView, AddTeamBotView, ModifyTeamBotView, RemoveTeamBotView


class TeamBotSite:
    def get_urls(self):
        urlpatterns = [
            path('all', AllTeamBotsView.as_view(), name="all"),
            path('<int:tround>/add', AddTeamBotView.as_view(), name="add"),
            path('<int:bot>/modify', ModifyTeamBotView.as_view(), name="modify"),
            path('<int:bot>/remove', RemoveTeamBotView.as_view(), name="remove"),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'bot', 'bot'


site = TeamBotSite()
