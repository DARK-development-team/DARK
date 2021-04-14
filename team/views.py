from django.shortcuts import render, redirect
from django.contrib import messages
from team.forms import *


def create_team_view(request):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        current_user = request.user
        if form.is_valid() and current_user.is_authenticated:
            team = form.save()

            # ensure that admin and default role is also present in db
            TeamRole.objects.create(team=team, name="Moderator", can_modify_members=True)
            TeamRole.objects.create(team=team, name="Member")
            creator_role = TeamRole.objects.create(team=team, name="Creator",
                                                   can_modify_members=True, can_remove=True)

            TeamMember.objects.create(team=team, user=current_user, role=creator_role)

            messages.success(request, f'Team created!')
            return redirect('Show Team Info', teamid=team.id)
    else:
        form = TeamCreationForm()

    return render(request, 'team/create.html', {'form': form})


def show_team_info_view(request, teamid):
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
    members = TeamMember.objects.filter(team=team)
    context = {
        "team": team,
        "members": members,
        "can_modify_members": can_modify_members,
        "can_remove": can_remove,
    }
    return render(request, 'team/info.html', context)


def remove_team_view(request, teamid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            member = TeamMember.objects.get(team=teamid, user=current_user.id)
            role = TeamRole.objects.get(id=member.role.id)
            can_remove = role.can_remove
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            can_remove = False
    else:
        can_remove = False

    if can_remove:
        team = Team.objects.get(id=teamid)
        if request.method == 'POST':
            team.delete()
            return redirect('Start Page')

        return render(request, 'team/remove.html', {'team': team})
    else:
        return redirect('Show Team Info', teamid=teamid)


def change_team_name_view(request, teamid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            member = TeamMember.objects.get(team=teamid, user=current_user.id)
            role = TeamRole.objects.get(id=member.role.id)
            can_remove = role.can_remove
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            can_remove = False
    else:
        can_remove = False

    if can_remove:
        team = Team.objects.get(id=teamid)

        if request.method == 'POST':
            form = ChangeTeamNameForm(request.POST)
            current_user = request.user
            if form.is_valid():
                team.name = form.cleaned_data.get('name')
                team.save()
                return redirect('Show Team Info', teamid=team.id)
        else:
            form = ChangeTeamNameForm()

        return render(request, 'team/change_name.html', {'form': form, 'team': team})
    else:
        return redirect('Show Team Info', teamid=teamid)


def manage_team_roles_view(request, teamid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            member = TeamMember.objects.get(team=teamid, user=current_user.id)
            role = TeamRole.objects.get(id=member.role.id)
            can_remove = role.can_remove
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            can_remove = False
    else:
        can_remove = False

    if can_remove:
        context = {
            "team": Team.objects.get(id=teamid),
            "roles": TeamRole.objects.filter(team_id=teamid)
        }
        return render(request, 'team/manage_roles.html', context)
    else:
        return redirect('Show Team Info', teamid=teamid)


def add_team_role_view(request, teamid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            member = TeamMember.objects.get(team=teamid, user=current_user.id)
            role = TeamRole.objects.get(id=member.role.id)
            can_remove = role.can_remove
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            can_remove = False
    else:
        can_remove = False

    if can_remove:
        if request.method == 'POST':
            form = AddTeamRoleForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                can_modify_members = form.cleaned_data.get('can_modify_members')
                can_remove = form.cleaned_data.get('can_remove')
                TeamRole.objects.create(team_id=teamid, name=name,
                                        can_modify_members=can_modify_members, can_remove=can_remove);
                messages.success(request, f'Role created!')
                return redirect('Manage Team Roles', teamid=teamid)
        else:
            form = AddTeamRoleForm()

    else:
        return redirect('Show Team Info', teamid=teamid)

    return render(request, 'team/add_role.html', {'form': form})


def modify_role_view(request, teamid, roleid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            member = TeamMember.objects.get(team=teamid, user=current_user.id)
            role = TeamRole.objects.get(id=member.role.id)
            can_remove = role.can_remove
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            can_remove = False
    else:
        can_remove = False

    if can_remove:
        if request.method == 'POST':
            form = ModifyTeamRoleForm(request.POST, instance=TeamRole.objects.get(id=roleid))
            if form.is_valid():
                form.save()
                messages.success(request, f'Role modified!')
                return redirect('Manage Team Roles', teamid=teamid)
        else:
            form = ModifyTeamRoleForm(instance=TeamRole.objects.get(id=roleid))
            print(form.fields)

    else:
        return redirect('Show Team Info', teamid=teamid)

    return render(request, 'team/modify_role.html', {'form': form})


def remove_role_view(request, teamid, roleid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            member = TeamMember.objects.get(team=teamid, user=current_user.id)
            role = TeamRole.objects.get(id=member.role.id)
            can_remove = role.can_remove
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            can_remove = False
    else:
        can_remove = False

    if can_remove:
        role = TeamRole.objects.get(id=roleid)
        if request.method == 'POST':
            role.delete()
            return redirect('Manage Team Roles', teamid=teamid)

        return render(request, 'team/remove_role.html', {'role': role})
    else:
        return redirect('Manage Team Roles', teamid=teamid)


def add_team_member_view(request, teamid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            member = TeamMember.objects.get(team=teamid, user=current_user.id)
            role = TeamRole.objects.get(id=member.role.id)
            can_modify_members = role.can_modify_members
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            can_modify_members = False
    else:
        can_modify_members = False

    if can_modify_members:
        if request.method == 'POST':
            form = AddTeamMemberForm(request.POST)
            form.fields['role'].queryset = TeamRole.objects.filter(team_id=teamid)
            if form.is_valid():
                team = Team.objects.get(id=teamid)
                user = form.cleaned_data.get('user')
                role = form.cleaned_data.get('role')
                TeamMember.objects.create(team=team, user=user, role=role)
                messages.success(request, f'Member added!')
                return redirect('Show Team Info', teamid=teamid)
        else:
            form = AddTeamMemberForm()
            form.fields['role'].queryset = TeamRole.objects.filter(team_id=teamid)

        return render(request, 'team/add_member.html', {'form': form})
    else:
        return redirect('Show Team Info', teamid=teamid)


def remove_team_member_view(request, teamid, teammemberid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            member = TeamMember.objects.get(team=teamid, user=current_user.id)
            role = TeamRole.objects.get(id=member.role.id)
            can_modify_members = role.can_modify_members
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            can_modify_members = False
    else:
        can_modify_members = False

    if can_modify_members:
        member = TeamMember.objects.get(user_id=teammemberid, team_id=teamid)
        if request.method == 'POST':
            member.delete()
            return redirect('Show Team Info', teamid=teamid)

        return render(request, 'team/remove_member.html', {'member': member})
    else:
        return redirect('Show Team Info', teamid=teamid)


def show_team_member_info_view(request, teamid, teammemberid):
    return redirect("Start Page")


def change_team_member_role_view(request, teamid, teammemberid):
    current_user = request.user
    if current_user.is_authenticated:
        try:
            member = TeamMember.objects.get(team=teamid, user=current_user.id)
            role = TeamRole.objects.get(id=member.role.id)
            can_modify_members = role.can_modify_members
        except (TeamMember.DoesNotExist, TeamRole.DoesNotExist):
            can_modify_members = False
    else:
        can_modify_members = False

    if can_modify_members:
        member = TeamMember.objects.get(team=teamid, user=teammemberid)
        if request.method == 'POST':
            form = ChangeRoleTeamMemberForm(request.POST, instance=member)
            form.fields['role'].queryset = TeamRole.objects.filter(team_id=teamid)
            if form.is_valid():
                form.save()
                messages.success(request, f'Member modified!')
                return redirect('Show Team Info', teamid=teamid)
        else:
            form = ChangeRoleTeamMemberForm(instance=member)
            form.fields['role'].queryset = TeamRole.objects.filter(team_id=teamid)

        return render(request, 'team/change_member_role.html', {'form': form,
                                                                'member': member})
    else:
        return redirect('Show Team Info', teamid=teamid)
