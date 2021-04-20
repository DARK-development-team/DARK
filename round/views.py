from django.shortcuts import render, redirect

from round.forms import RoundForm
from round.models import Round
from tournament.models import Tournament

from round import round_utils


def show_round_terms_view(request, tournamentid, roundid):
    if request.method == 'POST':
        round_utils.execute_round()

    round = Round.objects.get(id=roundid)

    context = {
        "round": round,
        "results": round_utils.get_round_results(),
    }
    return render(request, 'round/details.html', context)


def add_round_view(request, tournamentid):
    if request.method == 'POST':
        form = RoundForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            tournament = Tournament.objects.get(id=tournamentid)

            round = Round(name=name, tournament=tournament, start_date=start_date, end_date=end_date)
            round.save()

            return redirect('Tournament Details', tournamentid)

    else:
        form = RoundForm()

    return render(request, 'round/create.html', {'form': form})
