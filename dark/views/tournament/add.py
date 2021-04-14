from django.views.generic import CreateView
from django.urls import reverse

from dark.models.tournament import Tournament
from dark.forms.tournament import AddTournamentForm


class AddTournamentView(CreateView):
    model = Tournament
    template_name = 'dark/tournament/add.html'
    form_class = AddTournamentForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(AddTournamentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('tournament:info', kwargs={
            'tournament': self.object.id
        })
