from django import forms


class QueueForm(forms.Form):
    name = forms.CharField(max_length=30, help_text="Required.")
    start_date = forms.DateTimeField(help_text="Required. Format: yyyy-MM-dd hh:mm:ss")
    end_date = forms.DateTimeField(help_text="Required. Format: yyyy-MM-dd hh:mm:ss")
