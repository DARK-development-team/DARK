from django.views.generic import RedirectView
from django.urls import reverse_lazy


class TeamMemberInfoView(RedirectView):
    url = reverse_lazy('home:page')
