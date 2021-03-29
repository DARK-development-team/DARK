from django.shortcuts import render

from tournament.models import Tournament


def start_page(request):
    return render(request, 'tournament/start_page.html')


def tournaments(request):
    context = {
        "tournaments": Tournament.objects.all()
    }
    return render(request, 'tournament/tournaments.html', context)


def tournament_details(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    context = {
        "tournament": tournament
    }
    return render(request, 'tournament/tournament_details.html', context)
