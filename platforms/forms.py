from django.forms import ModelForm
from platforms.models import Platform


class PlatformForm(ModelForm):
    class Meta:
        model = Platform
        fields = ['name', 'address', 'commit', 'package_to_run']
