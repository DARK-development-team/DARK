from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateTimeInput, IntegerField
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

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date < timezone.now():
            raise ValidationError("The start date cannot be in the past!")
        if end_date < start_date:
            raise ValidationError("The end date cannot be earlier than the start date!")
