from django.forms import ModelForm, DateTimeInput
from django.utils import timezone


class TimePeriodForm(ModelForm):
    class Meta:
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        now = timezone.now()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date <= now:
            self.add_error('start_date', 'Start date must be in the future')
        if start_date >= end_date:
            self.add_error('end_date', 'End date must be after start date')

        return cleaned_data
