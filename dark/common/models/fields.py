import os
import shutil
import subprocess
import pickle
import threading
from datetime import datetime
from dark.common.git import remove_git_repo

from django.db.models.fields import Field
from django.db.models.fields.files import FileField

import dark.common.forms.fields as fields
from dark.common.validators import GitRepoValidator

from dark.common.gitrepo import GitRepo


class GitRepoField(Field):
    default_validators = [GitRepoValidator()]

    description = "Field representing local git repository checked out at specific commit"

    def __init__(self, local_directory='', *args, **kwargs):
        self.local_directory = local_directory
        kwargs['max_length'] = 256
        super(GitRepoField, self).__init__(*args, **kwargs)

    def generate_local_directory_name(self, instance):
        if callable(self.local_directory):
            local_directory_path = self.local_directory(instance)
        else:
            local_directory_path = datetime.now().strftime(str(self.local_directory))
        return local_directory_path

    def deconstruct(self):
        name, path, args, kwargs = super(GitRepoField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if not isinstance(value, str):
            return None
        url, commit, local_directory = value.split('\t')
        return GitRepo(url, commit, local_directory)

    def to_python(self, value):
        value = pickle.loads(value)
        if isinstance(value, GitRepo):
            return value
        if value is None:
            return value
        url, commit = value
        return GitRepo(super().to_python(url), super().to_python(commit), None)

    def get_prep_value(self, value):
        prep_url = super(GitRepoField, self).get_prep_value(value.url)
        prep_commit = super(GitRepoField, self).get_prep_value(value.commit)
        prep_local_directory = super(GitRepoField, self).get_prep_value(value.local_directory)
        if prep_local_directory is not None:
            return '\t'.join([prep_url, prep_commit, prep_local_directory])
        else:
            return '\t'.join([prep_url, prep_commit])

    def _clone(self, url, commit, local_directory):
        if os.path.exists(local_directory):
            remove_git_repo(local_directory)
        subprocess.call(['git', 'clone', url, local_directory])
        subprocess.call(['git', 'checkout', commit], cwd=local_directory)

    def pre_save(self, model_instance, add):
        gitrepo = super().pre_save(model_instance, add)
        local_directory = self.generate_local_directory_name(model_instance)
        gitrepo.local_directory = local_directory
        t = threading.Thread(target=self._clone, args=[gitrepo.url, gitrepo.commit, local_directory])
        t.setDaemon(True)
        t.start()
        return gitrepo

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def get_internal_type(self):
        return 'CharField'

    def formfield(self, **kwargs):
        return fields.GitRepoField()