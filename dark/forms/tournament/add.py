from django.forms import ModelForm, DateTimeInput

from dark.models.tournament import Tournament


class AddTournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
