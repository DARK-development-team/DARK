from django.forms import ModelForm

from dark.models.tournament.team import TeamRole


class ModifyTeamRoleForm(ModelForm):
    class Meta:
        model = TeamRole
        fields = ['name', 'can_modify_members', 'can_remove']
        labels = {
            "name": "New Name"
        }
