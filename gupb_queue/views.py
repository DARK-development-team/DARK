from django.shortcuts import render, redirect

from gupb_queue.forms import QueueForm
from gupb_queue.models import Queue
from platforms.models import Platform
from tournament.models import Tournament

from . import queue_utils
from platforms import platform_utils


def show_queue_terms_view(request, queue_id):
    if request.method == 'POST':
        queue_utils.execute_queue(queue_id)

    queue = Queue.objects.get(pk=queue_id)
    context = {
        "queue": queue,
        "results": queue_utils.get_queue_results(queue_id),
    }
    return render(request, 'gupb_queue/queue_details.html', context)


def add_queue_view(request, tournament_id):
    if request.method == 'POST':
        form = QueueForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            platform = Platform.objects.get(name=form.cleaned_data.get('platform'))
            tournament = Tournament.objects.get(pk=tournament_id)

            queue = Queue(name=name, tournament=tournament, start_date=start_date, end_date=end_date, platform=platform)
            queue.save()

            platform_utils.clone_repo(f'{platform.name}_{queue.pk}', platform.address, platform.commit)

            return redirect('Tournament Details', tournament_id)

    else:
        form = QueueForm()

    return render(request, 'gupb_queue/queue_form.html', {'form': form})
