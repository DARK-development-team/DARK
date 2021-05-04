from django.forms import ModelForm

from dark.models.platform.platform import Platform


class AddPlatformForm(ModelForm):
    class Meta:
        model = Platform
        fields = ['name', 'address', 'commit', 'package_to_run']
