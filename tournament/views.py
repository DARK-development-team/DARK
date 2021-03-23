from django.shortcuts import render

from tournament.models import Queue


def start_page(request):
    context = {
        "queues": Queue.objects.all()
    }
    return render(request, 'tournament/start_page.html')


def queue_requirements(request, queueid):
    queue = Queue.objects.get(pk=queueid)
    context = {
            "queue": queue
    }
    print(queue.title)
    return render(request, 'tournament/queue_details.html', context)
