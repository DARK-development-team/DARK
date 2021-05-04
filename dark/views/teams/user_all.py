from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView

from dark.models.tournament.team import Team


class UserAllTeamsView(LoginRequiredMixin, TemplateView):
    template_name = 'dark/teams/user_all.html'
    login_url = reverse_lazy('user:login')
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        now = timezone.now()
        teams = Team.objects.filter(teammember__user__username=current_user)
        return {
            "upcoming_teams": teams.filter(tournament__start_date__gt=now),
            "in_progress_teams": teams.filter(tournament__start_date__lte=now).filter(tournament__end_date__gt=now),
            "archived_teams": teams.filter(tournament__end_date__lte=now)
        }
