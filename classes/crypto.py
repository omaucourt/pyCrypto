import requests
import pprint as p


class CryptoPrice:
    def __init__(self, currency="usd"):
        self.currency = currency

    def get_xrp_value(self):
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "ripple", "vs_currencies": self.currency}
        response = requests.get(url, params=params)
        data = response.json()
        p.pprint(data)
        return data["ripple"][self.currency]

    def get_xrp_value_at_datetime(self, date, time):
        url = "https://api.coingecko.com/api/v3/coins/ripple/history"
        datetime_str = f"{date}T{time}"
        params = {"date": datetime_str}
        response = requests.get(url, params=params)
        data = response.json()
        p.pprint(data)
        return data["market_data"]["current_price"][self.currency]
