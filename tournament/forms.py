from django import forms


class TournamentForm(forms.Form):
    name = forms.CharField(max_length=100, help_text="Required.")
    start_date = forms.DateTimeField(help_text="Required. Format: yyyy-MM-dd hh:mm:ss")
    end_date = forms.DateTimeField(help_text="Required. Format: yyyy-MM-dd hh:mm:ss")
