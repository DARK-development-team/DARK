from django.forms import ModelForm

from dark.models.tournament.team import TeamMember


class ChangeTeamMemberRoleForm(ModelForm):
    class Meta:
        model = TeamMember
        fields = ['role']
        labels = {
            "role": "New role"
        }
