import requests
import pprint as p


class CryptoPrice:
    def __init__(self, currency="usd"):
        self.currency = currency

    def get_xrp_value(self):
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "ripple", "vs_currencies": self.currency}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            p.pprint(data)
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
