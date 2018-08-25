from django import forms
from django.core.exceptions import ValidationError

from services.models import ServiceType, ServiceRequest
from django.utils.translation import ugettext as _


class AddServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = '__all__'


class MakeRequestForm(forms.ModelForm):
    currency = forms.CharField(required=False, disabled=True)

    class Meta:
        model = ServiceRequest
        fields = ['amount', 'currency', 'description']
        widgets = {
            'amount': forms.TextInput()
        }


def validate_sheba(value):

    INVALID_SHEBA_MESSAGE = _("Invalid sheba number")

    if len(value) != 26:
        raise ValidationError(INVALID_SHEBA_MESSAGE)
    if value[:2] != "IR":
        raise ValidationError(INVALID_SHEBA_MESSAGE)
    middle_code = value[4:] + "1827" + value[2:4]
    try:
        middle_code = int(middle_code)
    except:
        raise ValidationError(INVALID_SHEBA_MESSAGE)
    if middle_code % 97 != 1:
        raise ValidationError(INVALID_SHEBA_MESSAGE)


class WithdrawRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput()
        }
    sheba = forms.CharField(label=_("Sheba number"), validators=[validate_sheba])

    def save(self, commit=True):
        obj = super(WithdrawRequestForm, self).save(commit=False)
        obj.description += self.cleaned_data["sheba"]

        if commit:
            obj.save()
        return obj


class RequestDetailsForm(forms.ModelForm):
    user = forms.CharField(required=False, disabled=True)
    amount = forms.CharField(required=False, disabled=True)
    currency = forms.CharField(required=False, disabled=True)
    description = forms.CharField(required=False, disabled=True)
    operator = forms.CharField(required=False, disabled=True)
    status = forms.CharField(required=False, disabled=True)

    class Meta:
        model = ServiceRequest
        fields = ['user', 'amount', 'currency', 'description', 'operator', 'status']
        field_classes = []

    def update(self, request, commit=True):
        if commit:
            request.save(force_update=True)
        return request
