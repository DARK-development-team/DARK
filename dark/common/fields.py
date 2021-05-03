import os.path
import subprocess

from django.core import checks
from django.db.models.fields import URLField
from django.db.models.fields.files import FileField

class FieldFile(File):
    def __init__(self, instance, field, name):
        super().__init__(None, name)
        self.instance = instance
        self.field = field
        self.storage = field.storage
        self._committed = True

    def __eq__(self, other):
        # Older code may be expecting FileField values to be simple strings.
        # By overriding the == operator, it can remain backwards compatibility.
        if hasattr(other, 'name'):
            return self.name == other.name
        return self.name == other

    def __hash__(self):
        return hash(self.name)

    # The standard File contains most of the necessary properties, but
    # FieldFiles can be instantiated without a name, so that needs to
    # be checked for here.

    def _require_file(self):
        if not self:
            raise ValueError("The '%s' attribute has no file associated with it." % self.field.name)

    def _get_file(self):
        self._require_file()
        if getattr(self, '_file', None) is None:
            self._file = self.storage.open(self.name, 'rb')
        return self._file

    def _set_file(self, file):
        self._file = file

    def _del_file(self):
        del self._file

    file = property(_get_file, _set_file, _del_file)

    @property
    def path(self):
        self._require_file()
        return self.storage.path(self.name)

    @property
    def url(self):
        self._require_file()
        return self.storage.url(self.name)

    @property
    def size(self):
        self._require_file()
        if not self._committed:
            return self.file.size
        return self.storage.size(self.name)

    def open(self, mode='rb'):
        self._require_file()
        if getattr(self, '_file', None) is None:
            self.file = self.storage.open(self.name, mode)
        else:
            self.file.open(mode)
        return self
    # open() doesn't alter the file's contents, but it does reset the pointer
    open.alters_data = True

    # In addition to the standard File API, FieldFiles have extra methods
    # to further manipulate the underlying file, as well as update the
    # associated model instance.

    def save(self, name, content, save=True):
        name = self.field.generate_filename(self.instance, name)
        self.name = self.storage.save(name, content, max_length=self.field.max_length)
        setattr(self.instance, self.field.attname, self.name)
        self._committed = True

        # Save the object because it has changed, unless save is False
        if save:
            self.instance.save()
    save.alters_data = True

    def delete(self, save=True):
        if not self:
            return
        # Only close the file if it's already open, which we know by the
        # presence of self._file
        if hasattr(self, '_file'):
            self.close()
            del self.file

        self.storage.delete(self.name)

        self.name = None
        setattr(self.instance, self.field.attname, self.name)
        self._committed = False

        if save:
            self.instance.save()
    delete.alters_data = True

    @property
    def closed(self):
        file = getattr(self, '_file', None)
        return file is None or file.closed

    def close(self):
        file = getattr(self, '_file', None)
        if file is not None:
            file.close()

    def __getstate__(self):
        # FieldFile needs access to its associated model field, an instance and
        # the file's name. Everything else will be restored later, by
        # FileDescriptor below.
        return {
            'name': self.name,
            'closed': False,
            '_committed': True,
            '_file': None,
            'instance': self.instance,
            'field': self.field,
        }

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.storage = self.field.storage


class GitRepoField(URLField):
    description = "Field representing cloned git repo"

    def __init__(self, local_directory='', **kwargs):
        self.local_directory = local_directory
        super().__init__(**kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_local_directory()
        ]

    def _check_local_directory(self):
        if os.path.isabs(self.local_directory):
            return [
                checks.Error(
                    "%s's 'local_directory' argument must be a relative path, not an "
                    "absolute path." % self.__class__.__name__,
                    obj=self,
                    id='fields.E202',
                    hint='Remove the leading slash.',
                )
            ]
        else:
            return []

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['local_directory'] = self.local_directory
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        subprocess.call(['git','clone', ])
        return file

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.attname, self.descriptor_class(self))

    def generate_filename(self, instance, filename):
        """
        Apply (if callable) or prepend (if a string) upload_to to the filename,
        then delegate further processing of the name to the storage backend.
        Until the storage layer, all file paths are expected to be Unix style
        (with forward slashes).
        """
        if callable(self.upload_to):
            filename = self.upload_to(instance, filename)
        else:
            dirname = datetime.datetime.now().strftime(str(self.upload_to))
            filename = posixpath.join(dirname, filename)
        return self.storage.generate_filename(filename)

    def save_form_data(self, instance, data):
        # Important: None means "no change", other false value means "clear"
        # This subtle distinction (rather than a more explicit marker) is
        # needed because we need to consume values that are also sane for a
        # regular (non Model-) Form to find in its cleaned_data dictionary.
        if data is not None:
            # This value will be converted to str and stored in the
            # database, so leaving False as-is is not acceptable.
            setattr(instance, self.name, data or '')

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.FileField,
            'max_length': self.max_length,
            **kwargs,
        })
