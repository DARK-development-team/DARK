from django.forms import ModelForm

from dark.models.tournament.team import TeamBot


class AddTeamBotForm(ModelForm):
    class Meta:
        model = TeamBot
        fields = ['bot', 'bot_package', 'bot_package_relative_wd', 'bot_symbol_name']
