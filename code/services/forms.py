from django.forms import ModelForm

from services.models import RequestType


class RequestTypeForm(ModelForm):
    class Meta:
        model = RequestType
        fields = ['short_name', 'name', 'currency', 'fee', 'status']
        #widgets = {
        #    'currency':
        #}

    def save(self, commit=True):
        pass
