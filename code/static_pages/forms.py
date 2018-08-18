from django import forms
from django.utils.translation import ugettext as _


class SendEmailToManagersForm(forms.Form):
    email = forms.EmailField(
        label=_("email"),
    )
    name = forms.CharField(
        label=_("name"),
        max_length=255,
    )
    text = forms.CharField(
        label=_("text"),
        widget=forms.Textarea,
    )
