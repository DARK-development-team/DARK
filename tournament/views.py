from django.shortcuts import render, redirect

from tournament.forms import TournamentForm
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
