from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse

from dark.models.tournament import TournamentRound, Tournament
from dark.forms.tournament import AddTournamentRoundForm
from dark.common.views import ForeignKeysMixin


class AddTournamentRoundView(ForeignKeysMixin, CreateView):
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

    def get_success_url(self):
        return reverse('tournament:tround:info', kwargs={
            'tournament': self.object.tournament.id,
            'tround': self.object.id
        })
