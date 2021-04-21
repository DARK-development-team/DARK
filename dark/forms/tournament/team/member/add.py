from django.forms import ModelForm

from dark.models.tournament.team import TeamMember


class AddTeamMemberForm(ModelForm):
    class Meta:
        model = TeamMember
        fields = ['user', 'role']
