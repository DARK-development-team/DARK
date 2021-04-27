from django.utils import timezone
from django.views.generic import TemplateView

from dark.common.views import UserAuthenticationDependentContextMixin
from dark.models.tournament import Tournament


class AllTournamentsView(UserAuthenticationDependentContextMixin, TemplateView):
    template_name = 'dark/tournament/all.html'

    def get_context_data(self, **kwargs):
        now = timezone.now()
        tournaments = Tournament.objects.filter(is_private=False)
        return {
            "upcoming_tournaments": tournaments.filter(start_date__gt=now),
            "in_progress_tournaments": tournaments.filter(start_date__lt=now, end_date__gt=now),
            "archived_tournaments": tournaments.filter(end_date__lte=now)
        }
