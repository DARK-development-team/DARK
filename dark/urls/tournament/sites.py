from django.urls import path

from . import tround
from . import team

from dark.views.tournament import AllTournamentsView, AddTournamentView, TournamentInfoView, UserAllTournamentsView, \
    AccessPrivateTournamentView


class TournamentSite:
    def get_urls(self):
        urlpatterns = [
            path('all', AllTournamentsView.as_view(), name="all"),
            path('add', AddTournamentView.as_view(), name='add'),
            path('<int:tournament>', TournamentInfoView.as_view(), name="info"),
            path('<int:tournament>/access', AccessPrivateTournamentView.as_view(), name='access'),
            path('<slug:username>/all', UserAllTournamentsView.as_view(), name='user all'),
            path('<int:tournament>/rounds/', tround.site.urls),
            path('<int:tournament>/teams/', team.site.urls),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'tournament', 'tournament'


site = TournamentSite()
