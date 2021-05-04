from django.urls import path

from dark.views.platform import AddPlatformView, PlatformInfoView


class PlatformSite:
    def get_urls(self):
        urlpatterns = [
            path('add', AddPlatformView.as_view(), name='add'),
            path('<int:platform>', PlatformInfoView.as_view(), name="info"),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'platform', 'platform'


site = PlatformSite()
