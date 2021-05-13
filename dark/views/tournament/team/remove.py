from django.contrib import messages
from django.views.generic import DeleteView
from django.urls import reverse

from dark.models.tournament.team import Team


class RemoveTeamView(DeleteView):
    model = Team
    template_name = 'dark/tournament/team/remove.html'
    context_object_name = 'team'
    slug_url_kwarg = 'team'
    slug_field = 'id'

    def delete(self, request, *args, **kwargs):
        get_kwargs = {
            self.slug_field: kwargs[self.slug_url_kwarg]
        }
        team = Team.objects.get(**get_kwargs)
        messages.success(self.request, 'Team ' + team.name + ' has successfully deleted!')
        return super(RemoveTeamView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('tournament:info', kwargs={
            'tournament': self.object.tournament.id
        })
