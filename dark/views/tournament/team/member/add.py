from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from dark.common.views import ForeignKeysMixin, FieldQuerySetMixin
from dark.forms.tournament.team import AddTeamMemberForm
from dark.models.tournament.team import TeamMember


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

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            team_id = kwargs.get('team')
            tournament_id = kwargs.get('tournament')
            return redirect(reverse('tournament:team:info', kwargs={
                'tournament': tournament_id,
                'team': team_id
            }))
        else:
            super(self)