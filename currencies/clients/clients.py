from requests import request
from decimal import Decimal


class GetCurrencyBaseClient:
    base_url = None
    curr_list = ('USD', 'EUR')

    def _request(self, method: str,
                 params: dict = None,
                 headers: dict = None,
                 data: dict = None):
        try:
            response = request(
                url=self.base_url,
                method=method,
                params=params or {},
                data=data or {},
                headers=headers or {}
            )
        except Exception:
            # TODO logging errors and success results
            ...
        else:
            return response.json()

    def _currencies(self,
                    code=None,
                    fields=None,
                    curr_list=None,
                    json=None):
        kurs = []
        for i in range(len(json)):
            for curr in curr_list:
                if json[i].get(fields[0]) == code.get(curr) and \
                   json[i].get(fields[1]) == code.get('UAH'):
                    buy = Decimal(
                        json[i].get(fields[2])).quantize(Decimal('1.00'))
                    sale = Decimal(
                        json[i].get(fields[3])).quantize(Decimal('1.00'))
                    kurs.append({
                        'currency': curr,
                        'buy': buy,
                        'sale': sale
                    })
        return kurs


class PrivatBankAPI(GetCurrencyBaseClient):
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'
    code = {
        'USD': 'USD',
        'EUR': 'EUR',
        'UAH': 'UAH'
    }
    fields = ('ccy', 'base_ccy', 'buy', 'sale')

    def get_currency(self) -> dict:
        json = self._request(
            'get',
            params={'json': '', 'exchange': '', 'coursid': 11}
        )
        return self._currencies(code=self.code,
                                fields=self.fields,
                                curr_list=self.curr_list,
                                json=json)


class MonoBankAPI(GetCurrencyBaseClient):
    base_url = 'https://api.monobank.ua/bank/currency'
    code = {
        'USD': 840,
        'EUR': 978,
        'UAH': 980
    }
    fields = ('currencyCodeA', 'currencyCodeB', 'rateBuy', 'rateSell')

    def get_currency(self) -> dict:
        json = self._request('get')
        return self._currencies(code=self.code,
                                fields=self.fields,
                                curr_list=self.curr_list,
                                json=json)


currency_clients = [
    PrivatBankAPI(),
    MonoBankAPI()
    ]

