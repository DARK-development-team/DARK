import os

from django.shortcuts import render
from django.views.generic import DetailView
from django.conf import settings
from django.http import HttpResponse, Http404

from dark.models.tournament import TournamentRound
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
        tround_execution.execute_round(TournamentRound.objects.get(**get_kwargs))

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'], context['log_file_path'], context['json_file_path'] =\
            tround_execution.get_round_results(self.object)
        print(os.getcwd())
        print(context['log_file_path'])
        return context