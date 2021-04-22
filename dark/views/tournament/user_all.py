from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView

from dark.common.views import UserAuthenticationDependentContextMixin
from dark.models.tournament import Tournament


class UserAllTournamentsView(UserAuthenticationDependentContextMixin, TemplateView):
    template_name = 'dark/tournament/user_all.html'

    def get_authenticated_context_data(self, **kwargs):
        current_user = self.request.user
        now = timezone.now()
        user_tournaments = Tournament.objects.filter(team__teammember__user=current_user)
        return {
            "upcoming_tournaments": user_tournaments.filter(start_date__gt=now),
            "in_progress_tournaments": user_tournaments.filter(start_date__lte=now).filter(end_date__gt=now),
            "archived_tournaments": user_tournaments.filter(end_date__lte=now)
        }

    def get_not_authenticated_context_data(self, **kwargs):
        redirect('login')
