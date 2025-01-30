import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from classes.currency import ExchangeRateCache
from classes.crypto import CryptoPrice


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
            input_field.textChanged.connect(self.update_conversions)
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

        # Set default value of 1 XRP
        self.currency_inputs["XRP"].setText("1")
        self.update_conversions()

    def refresh_conversion_rates(self):
        self.exchange_rate_cache = ExchangeRateCache()
        self.exchange_rate_data = self.exchange_rate_cache.get_exchange_rate(True)
        print(f"Exchange Rates: {self.exchange_rate_data}")  # Debug print
        self.update_conversions()

    def refresh_xrp_value(self):
        self.crypto_price = CryptoPrice(currency="usd")
        self.xrp_value = self.crypto_price.get_xrp_value()
        print(f"XRP Value: {self.xrp_value}")  # Debug print
        self.update_conversions()

    def update_conversions(self):
        amount = 1.0
        base_currency = "XRP"

        try:
            for currency in self.currencies:
                if self.currency_inputs[currency].hasFocus():
                    print(f"Currency: {currency}")
                    print(f"Amount: {self.currency_inputs[currency].text()}")
                    amount = float(self.currency_inputs[currency].text())
                    base_currency = currency
                    break
            else:
                print("No currency input focused")
                if self.currency_inputs["XRP"].text() == "0":
                    print("Amount is 0")
                    amount = 1.0
                else:
                    amount = float(self.currency_inputs["XRP"].text())

                print(f"Amount: {self.currency_inputs['XRP'].text()}")
                # amount = float(self.currency_inputs["XRP"].text())
                base_currency = "XRP"
        except ValueError:
            amount = 1.0
            base_currency = "XRP"

        print(f"Base Currency: {base_currency}, Amount: {amount}")

        if self.xrp_value is not None and self.exchange_rate_data is not None:
            print(f"XRP_VALUE ==> {self.xrp_value}")
            if base_currency == "XRP":
                xrp_amount = amount
            else:
                xrp_amount = amount / self.xrp_value

            print(f"XRP Amount: {xrp_amount}")

            for target_currency in self.currencies:
                if target_currency == "XRP":
                    self.currency_inputs[target_currency].setText(f"{xrp_amount:.4f}")
                else:
                    if target_currency in self.exchange_rate_data:
                        converted_amount = xrp_amount * self.exchange_rate_data[target_currency]
                        print(f"Converted Amount for {target_currency}: {converted_amount}")
                        self.currency_inputs[target_currency].setText(f"{converted_amount:.4f}")
                    else:
                        print(f"Exchange rate for {target_currency} not found.")
                        self.currency_inputs[target_currency].setText("N/A")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = CryptoConverter()
    converter.show()
    sys.exit(app.exec())
