from django import forms

from services.models import ServiceType, ServiceRequest


class AddServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = '__all__'


class MakeRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['amount', 'description']
        widgets = {
            'amount': forms.TextInput()
        }