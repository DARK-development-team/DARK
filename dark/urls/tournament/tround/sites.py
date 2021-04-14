from django.urls import path

from dark.views.tournament.tround import AddTournamentRoundView, TournamentRoundInfoView

class TournamentRoundSite:
    def get_urls(self):
        urlpatterns = [
            path('add', AddTournamentRoundView.as_view(), name="add"),
            path('<int:tround>', TournamentRoundInfoView.as_view(), name="info"),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'tround', 'tround'


site = TournamentRoundSite()
