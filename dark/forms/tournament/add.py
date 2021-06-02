from django.forms import IntegerField

from dark.common.forms.forms import TimePeriodForm
from dark.models.tournament import Tournament


class AddTournamentForm(TimePeriodForm):
    class Meta(TimePeriodForm.Meta):
        model = Tournament
        fields = ['name', 'start_date', 'end_date', 'is_private']

    number_of_teams = IntegerField(min_value=0, max_value=100, initial=0)
