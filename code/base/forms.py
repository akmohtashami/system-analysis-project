from django import forms

from base.models import Config


class EditIndexForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = ["index_content"]