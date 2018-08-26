from django import forms
from django.utils.translation import ugettext as _

from static_pages.models import StaticPage


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


class AddPageForm(forms.ModelForm):
    class Meta:
        model = StaticPage
        fields = '__all__'

    def save(self, commit=True):
        page = super(AddPageForm, self).save(commit=False)
        if commit:
            page.save()
        return page


class EditPageForm(forms.ModelForm):
    class Meta:
        model = StaticPage
        fields = ['name', 'text', 'is_visible']
        field_classes = []

    def update(self, page, commit=True):
        if commit:
            page.save(force_update=True)
        return page
