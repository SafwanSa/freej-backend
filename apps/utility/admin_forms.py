from .models import *
from django import forms
from apps.account.models import GroupEnum


class ConfigAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.config = kwargs.pop('config', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        user = self.request.user
        if self.config:
            is_system = self.config.is_system
            is_allowed = user.groups.filter(name=GroupEnum.Admin.value).exists()

            if not is_allowed and is_system:
                raise forms.ValidationError(
                    {'value': 'You have to have an Admin role to be able to change this setting.'})
        else:
            is_allowed = user.groups.filter(name=GroupEnum.Admin.value).exists()
            if not is_allowed:
                raise forms.ValidationError({
                    'key': 'You have to have an Admin role to be able to add a new config.',
                    'value': 'You have to have an Admin role to be able to add a new config.',
                    'description': 'You have to have an Admin role to be able to add a new config.',
                    'is_system': 'You have to have an Admin role to be able to add a new config.',
                    'is_private': 'You have to have an Admin role to be able to add a new config.',
                    'tag': 'You have to have an Admin role to be able to add a new config.',
                })
        return self.cleaned_data

    class Meta:
        model = Config
        exclude = [id]
