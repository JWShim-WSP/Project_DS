from django.shortcuts import render
#from django.conf import settings
#from djmoney.money import Money
import json

Currencies = {
    "AUD":"Australian Dollar",
    "BRL":"Brazilian Real",
    "BTC":"Bitcoin",
    "CAD":"Canadian Dollar",
    "CNY":"Chinese Yuan",
    "EUR":"Euro",
    "GBP":"British Pound Sterling",
    "HKD":"Hong Kong Dollar",
    "INR":"Indian Rupee",
    "JPY":"Japanese Yen",
    "KRW":"South Korean Won",
    "RUB":"Russian Ruble",
    "SGD":"Singapore Dollar",
    "THB":"Thai Baht",
}

def CurrencyExchangeService(request):
    return render(request, 'excurrency/excurrency.html',{
        "Currencies": Currencies
    })


"""
class CurrencyExchangeService:
    def get_rates_from_api(self, base_currency):
        url = f'{settings.CURRENCY_RATES_URL}?base={base_currency}'
        return requests.get(url).json()

    def get_rate(self, base_currency, currency):
        return self.get_rates_from_api(base_currency)['rates'][currency]
      
    def get_converted_amount(amount, base_currency, converted_currency):
        return round(float(amount) * float(self.get_rate(base_currency.upper(), converted_currency.upper())), 3)
      
    def validate_money(money):
        if not isinstance(money, Money):
            raise Exception('A Money instance must be provided')

    def convert(self, money, currency):
        self.validate_money(money)
        
        amount = money.amount
        base_currency = str(money.currency)
        converted_currency = str(currency)
        
        if base_currency.upper() == converted_currency.upper():
            return money
        return Money(self.get_converted_amount(amount, base_currency, converted_currency), converted_currency)
"""