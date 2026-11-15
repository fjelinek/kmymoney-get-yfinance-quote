# Copyright (C) 2026 Frank Jelinek
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import math
import sys
from datetime import datetime
import yfinance as yf


def get_fx_rate_to_eur(currency: str) -> float:
    """Fetch exchange rate from given currency to EUR."""
    currency_raw = currency.strip()
    currency_upper = currency_raw.upper()

    # Handle pence and sub-units
    unit_multiplier = 1.0
    if currency_raw == "GBp":
        fx_currency = "GBP"
        unit_multiplier = 0.01
    elif currency_raw == "ILA":
        fx_currency = "ILS"
        unit_multiplier = 0.01
    elif currency_raw == "ZAc":
        fx_currency = "ZAR"
        unit_multiplier = 0.01
    else:
        fx_currency = currency_upper

    if fx_currency == "EUR":
        return 1.0 * unit_multiplier

    rate_symbol = f"{fx_currency}EUR=X"
    rate_ticker = yf.Ticker(rate_symbol)

    rate = None
    # 1. Fast path: fast_info
    try:
        rate = rate_ticker.fast_info.last_price
    except Exception:
        pass

    # Validate rate
    if rate is not None:
        try:
            rate = float(rate)
            if math.isnan(rate) or rate <= 0:
                rate = None
        except (ValueError, TypeError):
            rate = None

    # 2. Fallback path: history
    if rate is None:
        try:
            hist = rate_ticker.history(period="1d")
            if not hist.empty:
                val = float(hist['Close'].iloc[-1])
                if not math.isnan(val) and val > 0:
                    rate = val
        except Exception:
            pass

    if rate is None or rate <= 0:
        raise ValueError(f"Could not determine exchange rate for {rate_symbol}")

    return rate * unit_multiplier


def fetch_quote(symbol: str) -> tuple[float, str]:
    """Fetch the latest price in EUR and quote date for a given symbol."""
    ticker = yf.Ticker(symbol)
    price = None
    currency = None

    # 1. Fast path: fast_info (much faster than ticker.info)
    try:
        fast = ticker.fast_info
        price = getattr(fast, 'last_price', None)
        currency = getattr(fast, 'currency', None)
    except Exception:
        pass

    # Check for valid numeric price
    if price is not None:
        try:
            price = float(price)
            if math.isnan(price) or price <= 0:
                price = None
        except (ValueError, TypeError):
            price = None

    # 2. Fallback path: ticker.history
    quote_date = None
    if price is None or currency is None:
        try:
            hist = ticker.history(period="1d")
            if not hist.empty:
                if price is None:
                    val = float(hist['Close'].iloc[-1])
                    if not math.isnan(val) and val > 0:
                        price = val
                quote_date = hist.index[-1].strftime('%Y-%m-%d')
        except Exception:
            pass

        # If currency is still missing, try ticker.info as last resort
        if currency is None:
            try:
                currency = ticker.info.get('currency')
            except Exception:
                pass

    if price is None:
        raise ValueError(f"Could not find price for {symbol}")
    if currency is None:
        raise ValueError(f"Could not determine currency for {symbol}")

    # 3. Currency conversion to EUR if needed
    eur_rate = 1.0
    if currency.upper() != 'EUR':
        eur_rate = get_fx_rate_to_eur(currency)

    eur_value = price * eur_rate
    date_str = quote_date or datetime.today().strftime('%Y-%m-%d')
    return eur_value, date_str


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <symbol>", file=sys.stderr)
        sys.exit(1)

    symbol = sys.argv[1].strip()

    try:
        eur_value, quote_date = fetch_quote(symbol)
        # Format required by KMyMoney: symbol;price;date
        print(f"{symbol};{eur_value:.4f};{quote_date}")
    except Exception as e:
        print(f"Error retrieving data for {symbol}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
