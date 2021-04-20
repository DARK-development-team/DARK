from django.shortcuts import render, redirect

from gupb_queue.models import Queue
from team.models import Team
from tournament.forms import TournamentForm
from tournament.models import Tournament

from django.utils import timezone


def tournaments(request):
    now = timezone.now()

    if request.user.is_authenticated:
        context = {
            "in_progress": Tournament.objects.filter(start_date__lt=now).filter(end_date__gt=now),
            "upcoming": Tournament.objects.filter(start_date__gt=now),
            "your_upcoming": Tournament.objects.filter(team__teammember__user_ID=request.user).filter(start_date__gt=now),
            "created_by_you": Tournament.objects.filter(creator=request.user),
        }
    else:
        context = {
            "in_progress": Tournament.objects.filter(start_date__lt=now).filter(end_date__gt=now),
            "upcoming": Tournament.objects.filter(start_date__gt=now),
            "your_upcoming": None,
            "created_by_you": None,
        }

    return render(request, 'tournament/tournaments.html', context)


def tournament_details(request, tournamentid):
    tournament = Tournament.objects.get(pk=tournamentid)
    queues = Queue.objects.filter(tournament=tournamentid)
    creator = True if tournament.creator == request.user else False

    context = {
        "tournament": tournament,
        "queues": queues,
        "contestants": Team.objects.filter(tournament_ID_id=tournamentid),
        "creator": creator
    }
    return render(request, 'tournament/tournament_details.html', context)


def tournament_add(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            creator = request.user

            tournament = Tournament(name=name, creator=creator, start_date=start_date, end_date=end_date)
            tournament.save()

            return redirect('Tournaments')

    else:
        form = TournamentForm()

    return render(request, 'tournament/tournament_form.html', {'form': form})
