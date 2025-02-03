import requests
import json
from datetime import datetime, timedelta
import os


class ExchangeRateCache:
    def __init__(self, cache_file="exchange_rate_cache.json"):
        self.cache_file = cache_file
        self.cache = None
        self.cache_time = None
        self.load_cache()

        # self.rates = {
        #     "USD": 1.0,  # Example rates
        #     "AUD": 1.61,
        #     "EUR": 0.96,
        # }

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as file:
                data = json.load(file)
                self.cache = data.get("cache")
                self.cache_time = datetime.fromisoformat(data.get("cache_time"))
        else:
            self.cache = None
            self.cache_time = None

    def save_cache(self):
        with open(self.cache_file, "w") as file:
            data = {"cache": self.cache, "cache_time": self.cache_time.isoformat()}
            json.dump(data, file)

    def get_exchange_rate(self, force_refresh=False):
        # return self.rates
        if force_refresh:
            self.cache = None
            self.cache_time = None

        if self.cache is None or self.cache_time is None or datetime.now() - self.cache_time > timedelta(minutes=25):
            print("Fetching new data")
            url = "https://v6.exchangerate-api.com/v6/35a6e535abc77be89695ace7/latest/USD"
            response = requests.get(url)
            if response.status_code == 200:
                self.cache = response.json()
                self.cache_time = datetime.now()
                self.save_cache()
            else:
                print("Error retrieving data")
                return None
        return self.cache["conversion_rates"]

    def convert_currency(self, amount, target_currency):
        # rate = self.rates.get(target_currency)
        # if rate:
        #     return amount * rate
        # return None

        if self.cache is None:
            print("Exchange rate data not available")
            return None
        rates = self.cache.get("conversion_rates", {})
        target_rate = rates.get(target_currency)
        if target_rate is None:
            print(f"Rate for {target_currency} not found")
            return None
        return amount * target_rate
