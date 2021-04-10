from django.shortcuts import render

from gupb_queue.models import Queue


def queue_details(request, tournament_id, queue_id):
    queue = Queue.objects.get(pk=queue_id)
    context = {
        "queue": queue
    }
    return render(request, 'gupb_queue/queue_details.html', context)
