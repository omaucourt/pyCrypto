import requests
from collections import OrderedDict
import pprint as p


class CryptoPrice:
    def __init__(self, currency="usd"):
        self.currency = currency

    def get_btc_to_currency(self, currencies=None):
        url = "https://api.coingecko.com/api/v3/exchange_rates"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            if currencies:
                filtered_data = {currency: data["rates"][currency] for currency in currencies if currency in data["rates"]}
                sorted_filtered_data = OrderedDict((currency, filtered_data[currency]) for currency in currencies if currency in filtered_data)
                return sorted_filtered_data
            else:
                return data["rates"]
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                raise Exception("Too Many Requests")
            print(f"Error fetching BTC to {self.currency} rate: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching BTC to {self.currency} rate: {e}")
            return None

    def convert_btc_to_xrp_based_currency(self):
        currencies = ["usd", "eur", "aud", "xrp", "btc", "eth", "link", "xlm"]
        btc_to_currency_list = self.get_btc_to_currency(currencies)

        if "xrp" not in btc_to_currency_list:
            print("Error: XRP value not found in the exchange rates")
            return None, None

        xrp_value = btc_to_currency_list["xrp"]["value"]
        print(f"XRP Value: {xrp_value}")

        btc_to_xrp_based_currency = OrderedDict((currency, btc_to_currency_list[currency]["value"] / xrp_value) for currency in currencies if currency in btc_to_currency_list)
        return btc_to_xrp_based_currency, xrp_value

    def get_xrp_value(self):
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "ripple", "vs_currencies": self.currency}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            print("---------------------------------------")
            p.pprint(data)
            print("---------------------------------------")
            return data["ripple"][self.currency]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching XRP value: {e}")
            return None

    def get_xrp_value_at_datetime(self, date, time):
        url = "https://api.coingecko.com/api/v3/coins/ripple/history"
        datetime_str = f"{date}T{time}"
        params = {"date": datetime_str}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            p.pprint(data)
            return data["market_data"]["current_price"][self.currency]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching XRP value at datetime: {e}")
            return None
