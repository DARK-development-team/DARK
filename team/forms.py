from django.forms import ModelForm
from team.models import *

class TeamCreationForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'tournament_ID']

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
        fields = ['user_ID', 'role_ID']

class ChangeRoleTeamMemberForm(ModelForm):
    class Meta:
        model = TeamMember
        fields = ['role_ID']
        labels = {
            "role_ID": "New role"
        }