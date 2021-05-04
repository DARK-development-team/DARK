from subprocess import Popen, PIPE

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class GitRepoValidator(URLValidator):
    def __init__(self, **kwargs):
        super(GitRepoValidator, self).__init__(**kwargs)

    def _is_remote_repository(self, url):
        lsremote = Popen(['git', 'ls-remote', url], stdout=PIPE)
        output, _ = lsremote.communicate()
        if lsremote.returncode != 0:
            return False
        else:
            return True

    def __call__(self, value):
        if not isinstance(value, str):
            value = value.url

        super(GitRepoValidator, self).__call__(value)

        if not self._is_remote_repository(value):
            raise ValidationError('Enter a valid git repository url', code=self.code, params={'value': value})
