import requests

from base.models import Config
from wallet.models import Currency


def get_exchange_rates():
    api_keys = {
        Currency.IRR: {
            Currency.USD: ("turkey_usd", 1),
            Currency.EUR: ("turkey_eur", 1),
        },
        Currency.USD: {
            Currency.IRR: ("turkey_usd", 0),
            Currency.EUR: ("diff_eur_usd", 1),
        },
        Currency.EUR: {
            Currency.IRR: ("turkey_eur", 0),
            Currency.USD: ("diff_eur_usd", 0)
        }
    }
    r = requests.get("http://call.tgju.org/ajax.json")
    api_result = r.json()["current"]

    response = {}
    currencies = list(Currency)
    for sell_cur in currencies:
        response[sell_cur] = {}
        for buy_cur in currencies:
            if sell_cur not in api_keys or buy_cur not in api_keys[sell_cur]:
                response[sell_cur][buy_cur] = None
                continue
            key, inverse = api_keys[sell_cur][buy_cur]
            response[sell_cur][buy_cur] = (1.0 / float(api_result[key]['p'])) if inverse else float(api_result[key]['p'])
    return response


def get_input_from_output_amount(input_currency, output_currency, output_amount):
    rates = get_exchange_rates()
    required_input = output_amount / rates[input_currency][output_currency]
    return required_input * (1 + (Config.get_solo().exchange_fee / 100.0))