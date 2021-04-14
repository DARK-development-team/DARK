from django.forms import ModelForm
from bots.models import *
from common.forms import BoundModelForm

class AddModifyBotForm(BoundModelForm):
    class Meta:
        model = Bot
        fields = ['bot_url']