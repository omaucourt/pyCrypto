import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from classes.currency import ExchangeRateCache
from classes.crypto import CryptoPrice
import pprint as p
from datetime import datetime


class CryptoConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.xrp_value = None
        self.exchange_rate_data = None

        self.crypto_price = CryptoPrice(currency="usd")
        self.filtered_rates, self.xrp_value = self.crypto_price.convert_btc_to_xrp_based_currency()
        self.exchange_rate_data = self.filtered_rates  # Set exchange_rate_data to filtered_rates

        print("-------------------------------------")
        p.pprint(self.filtered_rates)
        print(f"XRP Value: {self.xrp_value}")
        print("-------------------------------------")

        self.initUI()

    def update_conversions(self):
        print("Updating conversions")
        sender = self.sender()
        if sender:
            source_currency = sender.objectName()
            try:
                amount = float(sender.text())
            except ValueError:
                amount = 0.0

            for target_currency in self.currency_inputs:
                if target_currency != source_currency:
                    input_field = self.currency_inputs[target_currency]
                    input_field.blockSignals(True)  # Temporarily block signals to avoid recursion
                    converted_value = self.convert_currency(source_currency, target_currency, amount)
                    if converted_value is not None:
                        formatted_value = f"{converted_value:.10f}"  # Format to 10 decimal places
                        input_field.setText(formatted_value)
                    input_field.blockSignals(False)  # Re-enable signals

    def initUI(self):
        self.setWindowTitle("Crypto Converter")
        self.layout = QVBoxLayout()

        # Currency Labels and Inputs
        self.currency_inputs = {}
        for currency, rate in self.filtered_rates.items():
            h_layout = QHBoxLayout()
            label = QLabel(currency.upper())

            formatted_rate = f"{rate:.10f}"  # Format to 10 decimal places

            input_field = QLineEdit(str(formatted_rate))
            input_field.setObjectName(currency.upper())
            input_field.textChanged.connect(self.update_conversions)
            h_layout.addWidget(label)
            h_layout.addWidget(input_field)
            self.layout.addLayout(h_layout)
            self.currency_inputs[currency.upper()] = input_field

        # Last Refresh Date and Time
        self.last_refresh_label = QLabel()
        self.layout.addWidget(self.last_refresh_label)
        self.update_last_refresh_time()

        # Buttons
        self.refresh_rates_button = QPushButton("Refresh Rates")
        self.refresh_rates_button.clicked.connect(self.refresh_conversion_rates)
        self.layout.addWidget(self.refresh_rates_button)

        self.setLayout(self.layout)

    def update_last_refresh_time(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.last_refresh_label.setText(f"Last Refresh: {now}")

    def refresh_conversion_rates(self):
        try:
            self.filtered_rates, self.xrp_value = self.crypto_price.convert_btc_to_xrp_based_currency()
            self.exchange_rate_data = self.filtered_rates  # Update exchange_rate_data

            if self.filtered_rates is not None:
                for currency, rate in self.filtered_rates.items():
                    if currency.upper() in self.currency_inputs:
                        input_field = self.currency_inputs[currency.upper()]
                        input_field.blockSignals(True)  # Temporarily block signals
                        formatted_rate = f"{rate:.10f}"  # Format to 10 decimal places
                        input_field.setText(formatted_rate)
                        input_field.blockSignals(False)  # Re-enable signals
                self.update_last_refresh_time()
        except Exception as e:
            if str(e) == "Too Many Requests":
                self.show_error_message("Too Many Requests", "You have made too many requests to the API. Please try again later.")

    def show_error_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def convert_currency(self, source_currency, target_currency, amount):
        if source_currency == "XRP":
            usd_value = amount * self.xrp_value
        else:
            exchange_rate = self.exchange_rate_data.get(source_currency.lower(), None)
            if exchange_rate is None:
                print(f"Exchange rate for {source_currency} not found.")
                return None
            usd_value = amount * exchange_rate

        if target_currency == "XRP":
            return usd_value / self.xrp_value
        else:
            exchange_rate = self.exchange_rate_data.get(target_currency.lower(), None)
            if exchange_rate is None:
                print(f"Exchange rate for {target_currency} not found.")
                return None
            return usd_value / exchange_rate


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = CryptoConverter()
    converter.show()
    sys.exit(app.exec())
