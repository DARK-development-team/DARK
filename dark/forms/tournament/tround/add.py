from django.forms import ModelForm, DateTimeInput

from dark.models.tournament import TournamentRound


class AddTournamentRoundForm(ModelForm):
    class Meta:
        model = TournamentRound
        fields = ['name', 'start_date', 'end_date', 'platform']
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
