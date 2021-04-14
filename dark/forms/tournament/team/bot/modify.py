from django.forms import ModelForm

from dark.models.tournament.team import TeamBot


class ModifyTeamBotForm(ModelForm):
    class Meta:
        model = TeamBot
        fields = ['bot_url']
