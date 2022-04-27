from .models import *
from django import forms
from .services import BuildingService


class BuildingAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        changed_data = super().clean()
        if 'supervisor' in self.changed_data:
            self.instance.supervisor = changed_data.get('supervisor')
            BuildingService.update_supervisor(building=self.instance)
        return changed_data

    class Meta:
        model = Building
        exclude = [id]
