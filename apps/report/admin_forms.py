from .models import *
from django import forms
# from .services import BuildingService


class ReportAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        changed_data = super().clean()
        if 'is_checked' in self.changed_data:
            is_checked = self.cleaned_data.get('is_checked')
            if is_checked:
                changed_data['checked_by'] = self.current_user
            else:
                changed_data['checked_by'] = None
        return changed_data

    class Meta:
        model = Report
        exclude = [id]
