from django.views.generic import UpdateView
from django.urls import reverse

from dark.common.views import FieldQuerySetMixin
from dark.models.tournament.team import TeamMember
from dark.forms.tournament.team import ChangeTeamMemberRoleForm


class ChangeTeamMemberRoleView(FieldQuerySetMixin, UpdateView):
    model = TeamMember
    form_class = ChangeTeamMemberRoleForm
    template_name = 'dark/tournament/team/member/change_role.html'
    context_object_name = 'member'
    slug_url_kwarg = 'member'
    slug_field = 'id'

    def get_queryset_for_field(self, field_name, queryset):
        if field_name == 'role':
            queryset = queryset.filter(team_id=self.kwargs['team'])
        return queryset

    def get_success_url(self):
        return reverse('tournament:team:info', kwargs={
            'tournament': self.object.team.tournament.id,
            'team': self.object.team.id
        })
