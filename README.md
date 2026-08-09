# KMyMoney Quote Fetcher

This script fetches the latest financial quotes from Yahoo Finance and formats them for integration with KMyMoney.

## Prerequisites

- Python 3
- `yfinance` library

Install dependencies:
```bash
pip install yfinance
```

## Usage

### `one-quote.py`

Fetches the latest price for a single symbol. If the symbol is quoted in a currency other than EUR, it automatically fetches the conversion rate and calculates the price in EUR.

**Command:**
```bash
python3 one-quote.py <symbol>
```

**Example:**
```bash
python3 one-quote.py AAPL
```

**Output Format:**
The script prints exactly one line to standard output:
`symbol;price;date`

Example output:
`AAPL;172.4500;2023-10-27`

- **symbol**: The ticker symbol passed as an argument.
- **price**: The price in EUR, formatted to 4 decimal places.
- **date**: Today's date in `YYYY-MM-DD` format.

All error messages and usage instructions are directed to `stderr`.
