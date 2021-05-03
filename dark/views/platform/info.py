from django.views.generic import DetailView

from dark.models.platform.platform import Platform


class PlatformInfoView(DetailView):
    model = Platform
    template_name = 'dark/platform/info.html'
    context_object_name = 'platform'
    slug_url_kwarg = 'platform'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
