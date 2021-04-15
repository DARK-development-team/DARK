from django import forms

from gupb_queue.models import Queue


class QueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ['name', 'start_date', 'end_date', 'platform']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
