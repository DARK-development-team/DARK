import json

from celery.result import AsyncResult
from django.http import HttpResponse
from django.views.generic import DetailView

from dark.models.platform.platform import Platform


class PlatformInfoView(DetailView):
    model = Platform
    template_name = 'dark/platform/info.html'
    context_object_name = 'platform'
    slug_url_kwarg = 'platform'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def poll_platform_state(request):
    """ A view to report the progress to the user """
    if 'job_progress_id' in request.GET:
        job_progress_id = request.GET['job_progress_id']
    else:
        return HttpResponse('No job id given.')

    job = AsyncResult(job_progress_id)
    data = job.result or job.state
    return HttpResponse(json.dumps(data), mimetype='application/json')
