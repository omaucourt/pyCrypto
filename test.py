import requests
import pprint as p


def get_exchange_rates(base_currency="USD", target_currencies=["EUR", "AUD"]):
    """
    Fetches exchange rates for a given base currency against a list of target currencies
    using the CoinGecko API.

    Args:
      base_currency: The base currency for the exchange rates (default: "USD").
      target_currencies: A list of target currencies to get exchange rates for.

    Returns:
      A dictionary containing exchange rates for each target currency.
    """

    url = f"https://api.coingecko.com/api/v3/exchange_rates/{base_currency}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()
    rates = data.get("rates", {})

    exchange_rates = {}
    for currency in target_currencies:
        if currency in rates:
            exchange_rates[currency] = rates[currency]
        else:
            exchange_rates[currency] = None
            print(f"Exchange rate for {currency} not found.")

    return exchange_rates


def get_xrp_usd_exchange_rate():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    xrp_usd_rate = data["ripple"]["usd"]
    return xrp_usd_rate


# Example usage
currencies = ["eur", "aud", "usd"]
currency_rates = get_exchange_rates()
xrp_usd_rate = get_xrp_usd_exchange_rate()

p.pprint(currency_rates)
print(f"XRP to USD exchange rate: {xrp_usd_rate}")
