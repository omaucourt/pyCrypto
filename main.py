import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from classes.currency import ExchangeRateCache
from classes.crypto import CryptoPrice
import pprint as p


class CryptoConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.xrp_value = None
        self.exchange_rate_data = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Crypto Converter")
        self.layout = QVBoxLayout()

        # Currency Labels and Inputs
        self.currencies = ["XRP", "USD", "AUD", "EUR"]
        self.currency_inputs = {}
        for currency in self.currencies:
            h_layout = QHBoxLayout()
            label = QLabel(currency)
            input_field = QLineEdit("0")
            input_field.textChanged.connect(self.update_conversions2)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            self.layout.addLayout(h_layout)
            self.currency_inputs[currency] = input_field

        # Buttons
        self.refresh_rates_button = QPushButton("Refresh Conversion Rates")
        self.refresh_rates_button.clicked.connect(self.refresh_conversion_rates)
        self.refresh_xrp_button = QPushButton("Refresh XRP Value")
        self.refresh_xrp_button.clicked.connect(self.refresh_xrp_value)
        self.layout.addWidget(self.refresh_rates_button)
        self.layout.addWidget(self.refresh_xrp_button)

        self.setLayout(self.layout)
        self.refresh_conversion_rates()
        self.refresh_xrp_value()

        self.init_conversion()

    def convert_currency(self, source_currency, target_currency, amount):
        if source_currency == "XRP":
            usd_value = amount * self.xrp_value
        else:
            exchange_rate = self.exchange_rate_data.get(source_currency, None)
            if exchange_rate is None:
                print(f"Exchange rate for {source_currency} not found.")
                return None
            usd_value = amount / exchange_rate

        if target_currency == "XRP":
            return usd_value / self.xrp_value
        else:
            exchange_rate = self.exchange_rate_data.get(target_currency, None)
            if exchange_rate is None:
                print(f"Exchange rate for {target_currency} not found.")
                return None
            return usd_value * exchange_rate

    def update_conversions2(self):
        for currency in self.currencies:
            if self.currency_inputs[currency].hasFocus():
                changed_currency = self.currency_inputs[currency].text()
                amount = float(changed_currency)

                # Convert to USD
                new_usd_value = self.convert_currency(currency, "USD", amount)
                if new_usd_value is not None:
                    self.currency_inputs["USD"].setText(str(new_usd_value))

                    # Update other currencies
                    for target_currency in self.currencies:
                        if target_currency != currency and target_currency != "USD":
                            target_currency_value = self.convert_currency("USD", target_currency, new_usd_value)
                            if target_currency_value is not None:
                                print(f"Target Currency: {target_currency} - Value: {target_currency_value}")
                                self.currency_inputs[target_currency].setText(str(target_currency_value))

                    # Update XRP value
                    xrp_value = self.convert_currency("USD", "XRP", new_usd_value)
                    if xrp_value is not None:
                        self.currency_inputs["XRP"].setText(str(xrp_value))

    def init_conversion(self):
        # Set default value of 1 XRP
        self.currency_inputs["XRP"].setText("1")

        for currency in self.currencies:
            if currency != "XRP":
                value = self.xrp_value * self.exchange_rate_data[currency]
                self.currency_inputs[currency].setText(str(value))
                print(f"Currency : {currency} --> {self.exchange_rate_data[currency]}")

    def refresh_conversion_rates(self):
        self.exchange_rate_cache = ExchangeRateCache()
        self.exchange_rate_data = self.exchange_rate_cache.get_exchange_rate(True)

        self.update_conversions2()

    def refresh_xrp_value(self):
        self.crypto_price = CryptoPrice(currency="usd")
        self.xrp_value = self.crypto_price.get_xrp_value()
        print(f"XRP Value: {self.xrp_value}")  # Debug print
        self.update_conversions2()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = CryptoConverter()
    converter.show()
    sys.exit(app.exec())
