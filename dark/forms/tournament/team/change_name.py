from django.forms import ModelForm

from dark.models.tournament.team import Team


class ChangeTeamNameForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        labels = {
            "name": "New Name"
        }
