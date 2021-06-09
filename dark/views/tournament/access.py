from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from dark.forms.tournament.access import AccessPrivateTournamentForm
from dark.models.tournament import Tournament


class AccessPrivateTournamentView(FormView):
    template_name = 'dark/tournament/access.html'
    form_class = AccessPrivateTournamentForm
    success_url = reverse_lazy('tournament:all')

    def form_valid(self, form):
        access_key = form.cleaned_data.get('access_key')
        tournament = get_object_or_404(Tournament, id=self.kwargs['tournament'])

        if access_key == tournament.access_key:
            if self.request.user not in tournament.participants.all():
                messages.info(self.request, 'You have gained an access to ' + tournament.name)
                tournament.participants.add(self.request.user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tournament:info', kwargs={
            'tournament': self.kwargs['tournament']
        })
