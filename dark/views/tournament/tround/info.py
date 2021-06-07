import threading

from django.contrib import messages
from django.shortcuts import render
from django.views.generic import DetailView
from dark.logic.platform_utils import get_platform_requirements
from dark.logic import tround_execution

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
        result = self.get(request, *args, **kwargs)

        get_kwargs = {
            self.slug_field: kwargs[self.slug_url_kwarg]
        }

        tround = TournamentRound.objects.get(**get_kwargs)
        threading.Thread(
            target=lambda: tround_execution.execute_round(tround)).start()
        messages.success(self.request, 'The round has been started, please wait for email notifications.')

        context = self.get_context_data()
        context['status'] = 'running'
        return render(request, self.template_name, context)

        # return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'], context['log_file_path'], context['json_file_path'] = \
            tround_execution.get_round_results(self.object)
        context['requirements'] = get_platform_requirements(self.object.platform)
        return context
