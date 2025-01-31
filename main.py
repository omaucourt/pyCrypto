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

        # self.update_conversions()

        self.init_conversion()

    def update_conversions2(self):
        for currency in self.currencies:
            if self.currency_inputs[currency].hasFocus():
                print(f"Currency: {currency}")
                changed_currency = self.currency_inputs[currency].text()
                print(f"Currency {currency}: {changed_currency}")

                # Get the exchange rate of dollars
                exchange_rate = self.exchange_rate_data[currency]
                print(f"Exchange Rate: {exchange_rate}")

                new_usd_value = float(changed_currency) / exchange_rate

                self.currency_inputs["USD"].setText(str(new_usd_value))

                # We are going through the currencies and updating the value of the currency based on the new USD value calculated. We are not changing the focused currency
                for target_currency in self.currencies:
                    if target_currency != currency and target_currency != "USD" and target_currency != "XRP":
                        target_currency_value = new_usd_value * self.exchange_rate_data[target_currency]
                        print(f"Target Currency: {target_currency} - Value: {target_currency_value}")
                        self.currency_inputs[target_currency].setText(str(target_currency_value))

                # For each of the currency that have not the focus, we will update their value by first calculating the value in dollars and then apply the exchange rate
                # for target_currency in self.currencies:
                #     if target_currency != currency:
                #         print(f"Target Currency: {target_currency}")
                #         if target_currency == "XRP":
                #             # target_currency_value = float(changed_currency) / self.xrp_value
                #             target_currency_value = 66666
                #             pass
                #         else:
                #             target_currency_value = float(changed_currency) / self.exchange_rate_data[currency]
                #             print(f"changed currency: {changed_currency} --> Exchange Rate: {self.exchange_rate_data[currency]} --> Target Currency Value: {target_currency_value}")
                #             print(f"Curr: {currency} - Target: {target_currency} - Value: {target_currency_value}")
                #         self.currency_inputs[target_currency].setText(str(target_currency_value))

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
        print(f"Exchange Rates: {self.exchange_rate_data}")  # Debug print
        # self.update_conversions()

    def refresh_xrp_value(self):
        self.crypto_price = CryptoPrice(currency="usd")
        self.xrp_value = self.crypto_price.get_xrp_value()
        print(f"XRP Value: {self.xrp_value}")  # Debug print
        # self.update_conversions()

    def update_conversions(self):
        print("Calling update_conversions")
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
