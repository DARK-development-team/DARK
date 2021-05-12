import pickle

from django.forms import MultiValueField, URLField, CharField, MultiWidget, TextInput

from dark.common.validators import GitRepoValidator


class GitRepoWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = [TextInput(),
                   TextInput()]
        super(GitRepoWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return pickle.loads(value)
        else:
            return ['', '']


class GitRepoField(MultiValueField):
    widget = GitRepoWidget

    def __init__(self, *args, **kwargs):
        fields = (
            URLField(
                error_messages={'incomplete': 'Enter git repository url.'},
                validators=[
                    GitRepoValidator(),
                ],
                max_length=128
            ),
            CharField(
                error_messages={'incomplete': 'Enter commit hash.'},
                validators=[],
                max_length=64
            ),
        )
        super().__init__(
            fields, *args, **kwargs
        )

    def compress(self, data_list):
        return pickle.dumps(data_list)
