from django.forms import ModelForm
from team.models import *


class TeamCreationForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'tournament']


class ChangeTeamNameForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        labels = {
            "name": "New Name"
        }


class RemoveTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['id']


class AddTeamRoleForm(ModelForm):
    class Meta:
        model = TeamRole
        fields = ['name', 'can_modify_members', 'can_remove']


class ModifyTeamRoleForm(ModelForm):
    class Meta:
        model = TeamRole
        fields = ['name', 'can_modify_members', 'can_remove']
        labels = {
            "name": "New Name"
        }


class AddTeamMemberForm(ModelForm):
    class Meta:
        model = TeamMember
        fields = ['user', 'role']


class ChangeRoleTeamMemberForm(ModelForm):
    class Meta:
        model = TeamMember
        fields = ['role']
        labels = {
            "role": "New role"
        }
