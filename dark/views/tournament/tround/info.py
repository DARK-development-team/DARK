import threading

from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from dark.logic import tround_execution
from dark.logic.platform_utils import get_platform_requirements
from dark.models.tournament import TournamentRound


class TournamentRoundInfoView(DetailView):
    model = TournamentRound
    template_name = 'dark/tournament/tround/info.html'
    context_object_name = 'tround'
    slug_url_kwarg = 'tround'
    slug_field = 'id'

    def get(self, request, *args, **kwargs):
        return super(TournamentRoundInfoView, self).get(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        self.get(request, *args, **kwargs)

        get_kwargs = {
            self.slug_field: kwargs[self.slug_url_kwarg]
        }

        tround = TournamentRound.objects.get(**get_kwargs)
        threading.Thread(
            target=lambda: tround_execution.execute_round(tround)).start()
        messages.info(self.request, 'The round has been started, please wait for email notifications.')

        context = self.get_context_data()
        context['status'] = 'running'
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tround = get_object_or_404(TournamentRound, id=self.kwargs['tround'])

        context['is_creator_viewing'] = True if tround.tournament.creator == self.request.user else False
        context['requirements'] = get_platform_requirements(self.object.platform)
        context['results'], context['log_file_path'], context['json_file_path'] = \
            tround_execution.get_round_results(self.object)
        return context
