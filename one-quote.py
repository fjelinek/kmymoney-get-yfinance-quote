import sys
from datetime import datetime
import yfinance as yf

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <symbol>", file=sys.stderr)
    sys.exit(1)

symbol = sys.argv[1]

try:
    ticker = yf.Ticker(symbol)
    info = ticker.info
    
    price = info.get('regularMarketPrice')
    currency = info.get('currency')
    
    if price is None or currency is None:
        # Try to get price from history if info is missing regularMarketPrice
        hist = ticker.history(period="1d")
        if not hist.empty:
            price = hist['Close'].iloc[-1]
        else:
            print(f"Error: Could not find price for {symbol}", file=sys.stderr)
            sys.exit(1)

    # Conversion to EUR if necessary
    eur_rate = 1.0
    if currency and currency != 'EUR':
        rate_symbol = f"{currency}EUR=X"
        rate_ticker = yf.Ticker(rate_symbol)
        eur_rate = rate_ticker.info.get('regularMarketPrice', 1.0)
    
    eur_value = price * eur_rate
    today = datetime.today().strftime('%Y-%m-%d')
    
    # Print Symbol, Price, Date to standard out
    print(f"{symbol};{eur_value:.4f};{today}")

except Exception as e:
    print(f"Error retrieving data for {symbol}: {e}", file=sys.stderr)
    sys.exit(1)
