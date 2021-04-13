from django import forms

from queue.models import Queue


class QueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
