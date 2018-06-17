from django import forms
from django.utils.translation import ugettext as _


class RialChargeForm(forms.Form):
    email = forms.EmailField(label=_("Receiver"), required=True)
    amount = forms.IntegerField(label=_("Amount"), min_value=1, required=True)
