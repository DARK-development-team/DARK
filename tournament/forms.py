from django import forms


class TournamentForm(forms.Form):
    name = forms.CharField(max_length=100, help_text="Required.")
    start_date = forms.DateTimeField(help_text="Required.")
    end_date = forms.DateTimeField(help_text="Required.")
