from django import forms

from round.models import Round


class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
