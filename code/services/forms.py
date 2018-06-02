from django.forms import ModelForm

from services.models import ServiceType


class AddServiceTypeForm(ModelForm):
    class Meta:
        model = ServiceType
        fields = ['short_name', 'name', 'currency', 'fee', 'is_active']
        #widgets = {
        #    'currency':
        #}

    def save(self, commit=True):
        service_type = super(AddServiceTypeForm, self).save(commit)
        return service_type
