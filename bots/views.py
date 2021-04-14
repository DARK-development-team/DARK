from django.shortcuts import render, redirect
from django.contrib import messages
from bots.forms import *
from team.models import *

def show_team_bots_view(request, teamid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            member = TeamMember.objects.get(team=teamid, user=current_user.id)
            can_modify_members = member.role.can_modify_members
            can_remove = member.role.can_remove

        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            can_modify_members = False
            can_remove = False
    else:
        can_modify_members = False
        can_remove = False

    team = Team.objects.get(id=teamid)
    rounds = Round.objects.filter(tournament=team.tournament)
    round_bot_pairs = []
    for round in rounds:
        try:
            bot = Bot.objects.get(round=round)
        except Bot.DoesNotExist:
            bot = None
        round_bot_pairs.append((round, bot))
    context = {
        "team": team,
        "round_bot_pairs": round_bot_pairs
    }
    return render(request, 'bots/all_team.html', context)

def manage_team_round_bot_view(request, teamid, botid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            TeamMember.objects.get(team=teamid, user=current_user.id)
            is_member = True
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            is_member = False
    else:
        is_member = False

    if is_member:
        if request.method == 'POST':
            form = AddModifyBotForm(request.POST, instance=Bot.objects.get(id=botid))
            if form.is_valid():
                form.save()
                messages.success(request, f'Bot modified!')
                return redirect('Show Team Bots', teamid=teamid)
        else:
            form = AddModifyBotForm(instance=Bot.objects.get(id=botid))

        return render(request, 'bots/modify.html', {'form': form})
    else:
        return redirect('Show Team Bots', teamid=teamid)

def add_team_bot_round_view(request, teamid, roundid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            TeamMember.objects.get(team=teamid, user=current_user.id)
            is_member = True
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            is_member = False
    else:
        is_member = False

    if is_member:
        if request.method == 'POST':
            form = AddModifyBotForm(request.POST)
            if form.is_valid():
                team = Team.objects.get(id=teamid)
                round = Round.objects.get(id=roundid)
                form.save(team=team, round=round)
                messages.success(request, f'Bot added!')
                return redirect('Show Team Bots', teamid=teamid)
        else:
            form = AddModifyBotForm()

        return render(request, 'bots/add.html', {'form': form})
    else:
        return redirect('Show Team Bots', teamid=teamid)

def remove_team_round_bot_view(request, teamid, botid):
    bot = Bot.objects.get(id=botid)
    if request.method == 'POST':
        bot.delete()
        return redirect('Show Team Bots', teamid=teamid)
    else:
        return render(request, 'bots/remove.html', {'bot': bot})