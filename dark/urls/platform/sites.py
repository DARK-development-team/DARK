from django.urls import path

from dark.views.platform import AddPlatformView, PlatformInfoView, poll_platform_state


class PlatformSite:
    def get_urls(self):
        urlpatterns = [
            path('add', AddPlatformView.as_view(), name='add'),
            path('<int:platform>', PlatformInfoView.as_view(), name="info"),
            path('<int:platform>/poll_state', poll_platform_state, name="poll_state"),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'platform', 'platform'


site = PlatformSite()
