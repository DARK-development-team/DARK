from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateTimeInput, IntegerField

from dark.models.tournament import Tournament


class AddTournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date', 'is_private']
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    number_of_teams = IntegerField()

    def clean(self):
        if self.cleaned_data.get('start_date') > self.cleaned_data.get('end_date'):
            self.add_error('start_date', 'Start date must be before end date')
            raise ValidationError('Start date must be before end date')
