from dark.common.forms.forms import TimePeriodForm
from dark.models.tournament import TournamentRound


class AddTournamentRoundForm(TimePeriodForm):
    class Meta(TimePeriodForm.Meta):
        model = TournamentRound
        fields = ['name', 'start_date', 'end_date', 'platform']
