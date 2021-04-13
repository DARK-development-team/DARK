from django import forms


class BoundModelForm(forms.ModelForm):
    def save(self, commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self.instance, key, value)
        super(forms.ModelForm, self).save(commit)
