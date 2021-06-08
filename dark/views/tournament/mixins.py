from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from dark.models.tournament import Tournament


class TournamentEditableMixin(object):
    def dispatch(self, request, *args, **kwargs):
        tournament = get_object_or_404(Tournament, id=self.kwargs['tournament'])
        now = timezone.now()

        if tournament.start_date < now or tournament.end_date < now:
            messages.error(request, 'Tournament is no longer editable!')
            return redirect(reverse('tournament:info', kwargs={'tournament': self.kwargs['tournament']}))
        else:
            return super().dispatch(request, *args, **kwargs)
