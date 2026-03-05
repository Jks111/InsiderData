import yfinance as yf

# Cache dictionary to store fetched prices during a single run
price_cache = {}


def get_current_price(symbol: str):
    """
    Fetch latest stock price and currency.

    Uses an in-memory cache so the same ticker
    is never requested from yfinance more than once
    during a program run.

    Returns:
        (price, currency)
    """

    if not symbol:
        return None, None

    # Check cache first
    if symbol in price_cache:
        return price_cache[symbol]

    try:
        ticker = yf.Ticker(symbol)
        print("Fetching price from Yahoo:", symbol)
        data = ticker.history(period="1d")

        if data.empty:
            return None, None

        price = float(data["Close"].iloc[-1])
        currency = ticker.info.get("currency", "UNKNOWN")

        result = (price, currency)

        # Save result to cache
        price_cache[symbol] = result

        return result

    except Exception:
        return None, None