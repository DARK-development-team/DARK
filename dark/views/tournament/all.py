from django.utils import timezone
from django.views.generic import TemplateView

from dark.common.views import UserAuthenticationDependentContextMixin
from dark.models.tournament import Tournament


class AllTournamentsView(UserAuthenticationDependentContextMixin, TemplateView):
    template_name = 'dark/tournament/all.html'

    def get_authenticated_context_data(self, **kwargs):
        now = timezone.now()
        return {
            'in_progress': Tournament.objects
                .filter(team__teammember__user_id=self.request.user)
                .filter(start_date__lt=now)
                .filter(end_date__gt=now),
            'upcoming': Tournament.objects
                .filter(team__teammember__user_id=self.request.user)
                .filter(start_date__gt=now),
            'created_by_you': Tournament.objects
                .filter(creator=self.request.user),
        }

    def get_not_authenticated_context_data(self, **kwargs):
        now = timezone.now()
        return {
            'in_progress': Tournament.objects
                .filter(start_date__lt=now)
                .filter(end_date__gt=now),
            'upcoming': Tournament.objects
                .filter(start_date__gt=now),
        }
