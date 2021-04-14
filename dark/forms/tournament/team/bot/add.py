from django.forms import ModelForm

from dark.models.tournament.team import TeamBot


class AddTeamBotForm(ModelForm):
    class Meta:
        model = TeamBot
        fields = ['bot_url']
