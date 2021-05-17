from django.forms import ModelForm, DateTimeInput, IntegerField, forms
from django.utils import timezone

from dark.models.tournament import Tournament


class AddTournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date', 'is_private']
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    number_of_teams = IntegerField(min_value=0, max_value=100, initial=0)

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.now():
            raise forms.ValidationError("The start date cannot be in the past!")
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if end_date < start_date:
            raise forms.ValidationError("The end date cannot be earlier than the start date!")
        return end_date
