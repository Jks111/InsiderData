from DataromaScraper import scrape_insider_data
from simulator import simulate_grouped_trades
from database import init_db, insert_simulation


def main():
    print("Starting... \n")
    
    init_db()
    
    #Step 1: Scrape data
    trades = scrape_insider_data()
    print(f"Total trades scraped: {len(trades)}")

    print("\nCLEAN OUTPUT:")
    for r in trades:
        print(r)

    #Step 2: Simulate purchases
    simulated = simulate_grouped_trades(trades, capital=1000.0)
    
    print(f"Total grouped simulations: {len(simulated)}\n")

    for trade in simulated:
        print("-----")
        print(f"Stock: {trade['symbol']}")
        print(f"Insider: {trade['insider']}")
        print(f"Weighted Avg Price: €{trade['weighted_avg_price']}")
        print(f"Simulated Shares: {trade['simulated_shares']}")
    
    print("\nDONE!")

    # Store in DB
    for trade in simulated:
        insert_simulation(trade)

    print("All simulations stored in database.")

if __name__ == "__main__":
    main()