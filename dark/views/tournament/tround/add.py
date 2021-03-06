from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from dark.common.views import ForeignKeysMixin
from dark.forms.tournament import AddTournamentRoundForm
from dark.models.tournament import Tournament
from dark.models.tournament import TournamentRound
from dark.views.tournament.tround.mixins import RoundAddableMixin


class AddTournamentRoundView(RoundAddableMixin, ForeignKeysMixin, CreateView):
    model = TournamentRound
    template_name = 'dark/tournament/tround/add.html'
    form_class = AddTournamentRoundForm
    url_kwargs = ['tournament']
    url_kwarg_fields = ['tournament']

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            tournament_id = kwargs.get('tournament')
            return redirect(reverse('tournament:info', kwargs={
                'tournament': tournament_id
            }))
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            tournament = get_object_or_404(Tournament, id=self.kwargs['tournament'])
            is_valid = True

            if tournament.start_date > start_date:
                form.add_error('start_date', 'Start date must be after: ' + tournament.start_date.__str__())
                is_valid = False

            if tournament.end_date < end_date:
                form.add_error('end_date', 'End date must be before: ' + tournament.end_date.__str__())
                is_valid = False

            return super(AddTournamentRoundView, self).form_valid(form) if is_valid \
                else super(AddTournamentRoundView, self).form_invalid(form)
        except IntegrityError as e:
            messages.error(self.request, f'Failed to add round - make sure that field values are valid')
            return super(AddTournamentRoundView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('tournament:tround:info', kwargs={
            'tournament': self.object.tournament.id,
            'tround': self.object.id
        })
