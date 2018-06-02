from django import forms
from django.utils.translation import ugettext as _

from users.models import User
from utils.forms import RepeatPasswordForm


class RegisterForm(forms.ModelForm, RepeatPasswordForm):
    class Meta:
        model = User
        fields = ['name', 'email', ]
        field_classes = []

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user