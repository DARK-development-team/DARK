from django.urls import path

from dark.views.teams import UserAllTeamsView


class TeamsSite:
    def get_urls(self):
        urlpatterns = [
            path('<slug:username>/all', UserAllTeamsView.as_view(), name='user all'),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'teams', 'teams'


site = TeamsSite()
