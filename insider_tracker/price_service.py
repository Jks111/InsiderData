import yfinance as yf


def get_current_price(symbol: str):
    """
    Fetches current stock price using yfinance.
    Returns None if fetch fails.
    """

    if not symbol:
        return None

    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")

        if data.empty:
            return None

        return float(data["Close"].iloc[-1])

    except Exception:
        return None