# KMyMoney Quotes

A collection of Python scripts to fetch financial quotes using `yfinance` and format them for import into KMyMoney.

## Prerequisites

- Python 3
- `yfinance` library

You can install `yfinance` using pip:
```bash
pip install yfinance
```

## Scripts

### `one-quote.py`

Fetches the latest price for a single symbol, converts it to EUR (if the symbol is in a different currency), and prints it to standard output.

**Usage:**
```bash
python3 one-quote.py <symbol>
```

**Example:**
```bash
python3 one-quote.py IE00B3VVMM84
```
**Output Format:**
`symbol;price;date` (e.g., `IE00B3VVMM84;123.4567;2023-10-27`)

### `quotes.py`

Fetches quotes for a predefined list of funds and prints them in CSV format.

**Usage:**
```bash
python3 quotes.py
```

**Output Format:**
`symbol,price,date`

## Integration with KMyMoney

These scripts are designed to be used with KMyMoney's online quote feature or CSV import. The `one-quote.py` script is particularly useful for fetching individual fund prices in a format that is easy to parse.
