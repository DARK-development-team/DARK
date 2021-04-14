from django.urls import path

from dark.views.home import HomePageView


class HomeSite:
    def get_urls(self):
        urlpatterns = [
            path('', HomePageView.as_view(), name='page'),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'home', 'home'


site = HomeSite()
