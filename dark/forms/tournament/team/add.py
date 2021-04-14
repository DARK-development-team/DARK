from django.forms import ModelForm

from dark.models.tournament.team import Team


class AddTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name']
