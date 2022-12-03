from currencies.models import CurrencyHistory
from currencies.tasks import get_currencies
from currencies.clients.clients import currency_clients


def test_get_currencies_task(mocker, faker):
    assert not CurrencyHistory.objects.exists()

    get_currency = mocker.patch('currencies.cliens.cliens.PrivatBankAPI.get_currency')

    get_currency.return_value = [
        {'currency': 'USD', 'buy': '2', 'sale': '3'},
        {'currency': 'EUR', 'buy': '4', 'sale': '5'},
    ]
    assert not get_currency.call_count
    get_currencies()

    assert get_currency.call_count
    assert CurrencyHistory.objects.filter(currency='USD', sale='3')
    assert CurrencyHistory.objects.filter(currency='EUR', sale='5')