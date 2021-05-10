from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView

from dark.models.tournament import Tournament


class UserAllTournamentsView(LoginRequiredMixin, TemplateView):
    template_name = 'dark/tournament/user_all.html'
    login_url = reverse_lazy('user:login')
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        now = timezone.now()
        user_tournaments = Tournament.objects.filter(participants__in=[current_user])
        return {
            "upcoming_tournaments": user_tournaments.filter(start_date__gt=now),
            "in_progress_tournaments": user_tournaments.filter(start_date__lte=now).filter(end_date__gt=now),
            "archived_tournaments": user_tournaments.filter(end_date__lte=now)
        }
