from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.utils.translation import ugettext as _

from users.models import User, UserType
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


class RegisterWithLinkForm(forms.ModelForm, RepeatPasswordForm):
    class Meta:
        model = User
        fields = ['name', ]
        field_classes = []

    def update(self, user, commit=True):
        if commit:
            user.save(force_update=True)
            user.set_password(self.cleaned_data.get("password1"))
            user.save(force_update=True)
        return user


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. "
            "Note that password is case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }


class ChangePasswordForm(SetPasswordForm):
    pass


class SendEmailToUsersForm(forms.Form):
    subject = forms.CharField(
        label=_("subject"),
        max_length=255,
    )
    text = forms.CharField(
        label=_("text"),
        widget=forms.Textarea,
    )


class AddUserForm(forms.ModelForm, RepeatPasswordForm):
    type = forms.ChoiceField(choices=UserType.choices())

    class Meta:
        model = User
        fields = ['name', 'email', 'type']
        field_classes = []

    def save(self, commit=True):
        user = super(AddUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    error_messages = {
        'customer_with_salary': _("Customer/admin monthly salary should be zero."),
    }
    type = forms.ChoiceField(choices=UserType.choices())

    class Meta:
        model = User
        fields = ['name', 'monthly_salary', 'type', 'is_active']
        field_classes = []

    def update(self, user, commit=True):
        if commit:
            user.save(force_update=True)
        return user

    def clean_monthly_salary(self):
        monthly_salary = self.cleaned_data.get("monthly_salary")
        type = self.data.get("type")
        if monthly_salary != 0 and type != 'Employee':
            raise forms.ValidationError(
                ProfileForm.error_messages['customer_with_salary'],
                code='customer_with_salary',
            )
        return monthly_salary
