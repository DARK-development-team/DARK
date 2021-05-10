from django import forms


class AccessPrivateTournamentForm(forms.Form):
    access_key = forms.IntegerField()
