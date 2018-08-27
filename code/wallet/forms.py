from django import forms
from django.utils.translation import ugettext as _

from base.models import Config
from wallet.models import Wallet
from wallet.utils import get_exchange_rates, get_input_from_output_amount


class RialChargeForm(forms.Form):
    email = forms.EmailField(label=_("Receiver"), required=True)
    amount = forms.FloatField(label=_("Amount"), min_value=0, widget=forms.TextInput(), required=True)


class CompanyRialChargeForm(forms.Form):
    amount = forms.FloatField(label=_("Amount"), min_value=0, widget=forms.TextInput(), required=True)


class ExchangeSimulationForm(forms.Form):
    input_amount = forms.FloatField(label=_("Input amount"), required=False, widget=forms.TextInput(), min_value=0)
    input_currency = Wallet._meta.get_field("currency").formfield(label=_("Input currency"), required=True, blank=False)
    output_amount = forms.FloatField(label=_("Output amount"), required=False, widget=forms.TextInput(), min_value=0)
    output_currency = Wallet._meta.get_field("currency").formfield(label=_("Output currency"), required=True, blank=False)

    def __init__(self, data=None, *args, **kwargs):
        self.calculate_first_currency = kwargs.pop("calculate_first_currency", None)
        super(ExchangeSimulationForm, self).__init__(data, *args, **kwargs)

    def clean(self):
        data = super(ExchangeSimulationForm, self).clean()
        if self.calculate_first_currency is None:
            return data
        if "input_currency" not in data or "output_currency" not in data:
            return data
        rates = get_exchange_rates()
        exchange_rate = rates[data["input_currency"]][data["output_currency"]]
        if exchange_rate is None:
            raise forms.ValidationError(_("This conversion is not possible"))
        if self.calculate_first_currency is True:
            if data.get("output_amount", None) is None:
                self.add_error("output_amount", _("This field is required"))
                return data
            final_input = \
                get_input_from_output_amount(
                    data["input_currency"],
                    data["output_currency"],
                    data["output_amount"]
                )
            data["input_amount"] = round(final_input, 2)

        else:
            if data.get("input_amount", None) is None:
                self.add_error("input_amount", _("This field is required"))
                return data
            if data.get("input_amount", None) is None:
                data["input_amount"] = 0
            real_input = data["input_amount"] / (1 + (Config.get_solo().exchange_fee / 100.0))
            final_output = real_input * exchange_rate
            data["output_amount"] = round(final_output, 2)
        return data


class ExchangeForm(forms.Form):
    input_currency = Wallet._meta.get_field("currency").formfield(label=_("Input currency"))
    output_currency = Wallet._meta.get_field("currency").formfield(label=_("Output currency"))
    output_amount = forms.FloatField(label=_("Output amount"), widget=forms.TextInput(), min_value=0)

    def clean(self):
        data = super(ExchangeForm, self).clean()
        if "input_currency" not in data or "output_currency" not in data:
            return data
        rates = get_exchange_rates()
        exchange_rate = rates[data["input_currency"]][data["output_currency"]]
        if exchange_rate is None:
            raise forms.ValidationError(_("This conversion is not possible"))
        return data


class ExchangeConfirmationForm(forms.Form):
    input_currency = Wallet._meta.get_field("currency").formfield(label=_("Input currency"))
    output_currency = Wallet._meta.get_field("currency").formfield(label=_("Output currency"))
    output_amount = forms.FloatField(label=_("Output amount"), widget=forms.TextInput(), min_value=0)
    input_amount = forms.FloatField(label=_("Input amount"), widget=forms.TextInput(), min_value=0)

    def clean(self):
        data = super(ExchangeConfirmationForm, self).clean()
        if "input_currency" not in data or "output_currency" not in data:
            return data
        rates = get_exchange_rates()
        exchange_rate = rates[data["input_currency"]][data["output_currency"]]
        if exchange_rate is None:
            raise forms.ValidationError(_("This conversion is not possible"))
        return data


class ReportForm(forms.Form):
    text = forms.CharField(
        label=_("text"),
        widget=forms.Textarea,
    )
