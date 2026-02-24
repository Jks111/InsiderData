from collections import defaultdict


def simulate_grouped_trades(trades: list, capital: float = 1000.0):
    """
    Groups insider purchases by (symbol, insider),
    calculates weighted average price,
    then simulates buying with fixed capital.
    """

    grouped = defaultdict(list)

    # Step 1: Group only purchases
    for trade in trades:
        if trade.get("trade_type") != "Purchase":
            continue

        key = (trade["symbol"], trade["insider"])
        grouped[key].append(trade)

    simulated_results = []

    # Step 2: Calculate weighted average + simulate
    for (symbol, insider), trade_list in grouped.items():

        total_shares = sum(t["shares"] for t in trade_list)
        total_amount = sum(t["amount"] for t in trade_list)

        if total_shares == 0:
            continue

        weighted_avg_price = total_amount / total_shares

        simulated_shares = capital / weighted_avg_price

        simulated_results.append({
            "symbol": symbol,
            "insider": insider,
            "company": trade_list[0]["company"],
            "total_insider_shares": total_shares,
            "weighted_avg_price": round(weighted_avg_price, 4),
            "simulated_shares": round(simulated_shares, 6),
            "capital_used": capital
        })

    return simulated_results