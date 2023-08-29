from flask import Flask, request, render_template
import requests

app = Flask(__name__)

currency_signs = {
    "USD": "$",
    "EUR": "€",
    "JPY": "¥",
    "GBP": "£",
    "AUD": "A$",
    "CAD": "C$",
    "CHF": "CHF",
    "CNY": "¥",
    "SEK": "kr",
    "NZD": "NZ$",
    "MXN": "$",
    "SGD": "S$",
    "HKD": "HK$",
    "NOK": "kr",
    "KRW": "₩",
    "TRY": "₺",
    "RUB": "₽",
    "INR": "₹",
    "BRL": "R$",
    "ZAR": "R",
    "PHP": "₱",
    "PLN": "zł",
    "THB": "฿",
    "IDR": "Rp",
    "HUF": "Ft",
    "CZK": "Kč",
    "ILS": "₪",
    "CLP": "$",
    "ISK": "kr",
    "DKK": "kr",
    "MYR": "RM",
    "RON": "lei",
    "HRK": "kn",
    "BGN": "лв",
    "UAH": "₴",
    "VND": "₫",
    "AED": "د.إ",
    "EGP": "E£",
    "COP": "$",
    "ARS": "$",
    "PKR": "₨",
    "KZT": "₸",
    "QAR": "ر.ق",
    "PEN": "S/",
    "NGN": "₦",
    "BDT": "৳",
    "BYN": "Br",
    "TWD": "NT$",
    "MAD": "د.م.",
    "DZD": "د.ج",
    "OMR": "ر.ع.",
    "LKR": "Rs",
    "BOB": "Bs.",
    "JOD": "د.ا",
    "KES": "KSh",
    "ZWL": "Z$",
    "IQD": "ع.د",
    "CRC": "₡",
    "PAB": "B/.",
    "ETB": "Br",
    "ISK": "kr",
    "PYG": "₲",
    "UZS": "so'm",
    "BHD": "ب.د",
    "GTQ": "Q",
    "IRR": "﷼",
    "SAR": "ر.س",
    "AMD": "֏",
    "NPR": "रू",
    "PKR": "₨",
    "TND": "د.ت",
    "GEL": "₾",
    # Add more currencies here as needed
}


def fetch_currency_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rates = data["rates"]
        available_currencies = list(rates.keys())
        return rates, available_currencies
    else:
        return None, None


def convert_currency(amount, from_currency, to_currency, rates):
    from_rate = rates.get(from_currency, 1.0)
    to_rate = rates.get(to_currency, 1.0)

    # Perform the conversion
    usd_amount = amount / from_rate  # Convert to USD first, if needed
    converted_amount = usd_amount * to_rate  # Convert to target currency

    return round(converted_amount, 2)


@app.route("/", methods=["GET", "POST"])
def index():
    rates, available_currencies = fetch_currency_rates()
    
    if rates is None or available_currencies is None:
        return "Error fetching rates, please try again later", 500
    
    if request.method == "POST":
        from_currency = request.form["from_currency"].upper()
        to_currency = request.form["to_currency"].upper()
        
        try:
            amount = float(request.form["amount"])
        except ValueError:
            return render_template(
                "index.html",
                error="Invalid amount. Please enter a numerical value.",
                available_currencies=available_currencies
            )
        
        # Check for negative numbers
        if amount < 0:
            return render_template(
                "index.html",
                error="Amount cannot be negative.",
                available_currencies=available_currencies
            )
        
        converted_amount = convert_currency(
            amount, from_currency, to_currency, rates
        )
        
        if converted_amount is not None:
            from_sign = currency_signs.get(from_currency, "")
            to_sign = currency_signs.get(to_currency, "")
            return render_template(
                "index.html",
                converted_amount=f"{from_sign}{amount} {from_currency} is {to_sign}{converted_amount} {to_currency}",
                available_currencies=available_currencies
            )
        else:
            return render_template(
                "index.html",
                error="Invalid currency codes. Please try again.",
                available_currencies=available_currencies
            )

    return render_template("index.html", available_currencies=available_currencies)


if __name__ == "__main__":
    app.run(debug=True)
