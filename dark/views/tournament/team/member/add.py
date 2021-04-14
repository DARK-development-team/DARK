from django.views.generic import CreateView
from django.urls import reverse

from dark.models.tournament.team import TeamMember
from dark.models.tournament.team import TeamRole
from dark.forms.tournament.team import AddTeamMemberForm
from dark.common.views import ForeignKeysMixin, FieldQuerySetMixin


class AddTeamMemberView(FieldQuerySetMixin, ForeignKeysMixin, CreateView):
    model = TeamMember
    template_name = 'dark/tournament/team/member/add.html'
    form_class = AddTeamMemberForm
    url_kwargs = ['team']
    url_kwarg_fields = ['team']

    def get_queryset_for_field(self, field_name, queryset):
        if field_name == 'role':
            queryset = queryset.filter(team_id=self.kwargs['team'])
        return queryset

    def get_success_url(self):
        return reverse('tournament:team:info', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id
        })
