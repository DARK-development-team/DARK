from django.shortcuts import render, redirect
from django.contrib import messages
from teams.models import *

def show_all_teams_view(request):
    context = {
        "teams": Team.objects.all(),
    }
    return render(request, 'teams/show_all.html', context)

def show_user_teams_view(request, userid):
    current_user = request.user
    if current_user.is_authenticated:
        context = {
            "teams": Team.objects.filter(teammember__user_ID_id=userid),
        }
        return render(request, 'teams/show_user_all.html', context)
    else:
        redirect("Login")

def show_all_tournament_teams_view(request, tournamentid):
    context = {
        "teams": Team.objects.filter(tournament_ID_id=tournamentid),
        "tournament": Tournament.objects.get(id=tournamentid),
    }
    return render(request, 'teams/show_tournament_all.html', context)
