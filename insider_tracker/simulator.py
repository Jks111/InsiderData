from collections import defaultdict
from .price_service import get_current_price


def simulate_grouped_trades(trades: list, capital: float = 1000.0):

    grouped = defaultdict(list)

    for trade in trades:
        if trade.get("trade_type") != "Purchase":
            continue

        key = (trade["symbol"], trade["insider"])
        grouped[key].append(trade)

    simulated_results = []

    for (symbol, insider), trade_list in grouped.items():

        total_shares = sum(t["shares"] for t in trade_list)
        total_amount = sum(t["amount"] for t in trade_list)

        if total_shares == 0:
            continue

        weighted_avg_price = total_amount / total_shares
        simulated_shares = capital / weighted_avg_price

        current_price = get_current_price(symbol)

        if current_price:
            current_value = simulated_shares * current_price
            profit = current_value - capital
            return_pct = (profit / capital) * 100
        else:
            current_value = None
            profit = None
            return_pct = None

        simulated_results.append({
            "symbol": symbol,
            "insider": insider,
            "company": trade_list[0]["company"],
            "total_insider_shares": total_shares,
            "weighted_avg_price": round(weighted_avg_price, 4),
            "simulated_shares": round(simulated_shares, 6),
            "capital_used": capital,
            "current_price": current_price,
            "current_value": round(current_value, 2) if current_value else None,
            "profit": round(profit, 2) if profit else None,
            "return_pct": round(return_pct, 2) if return_pct else None
        })

    return simulated_results