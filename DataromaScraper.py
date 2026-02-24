import requests
from bs4 import BeautifulSoup

URL = "https://dataroma.com/m/ins/ins.php"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}


def scrape_insider_data():
    print("connecting...")

    response = requests.get(URL, headers=headers)
    print("Status", response.status_code)

    if response.status_code != 200:
        print("Failed to load")
        return []

    print("Scraper running...")
    
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", id="grid")

    if not table:
        print("Table with id='grid' not found.")
        return []

    rows = table.find_all("tr")

    data_rows = rows[1:]  # skip header
    limit = min(50, len(data_rows))

    print(f"Processing {limit} rows.")

    data = []

    for row in data_rows[:limit]:
        symbol = row.find("td", class_="iss_sym")
        company = row.find("td", class_="iss_name")
        insider = row.find("td", class_="rep_name")
        relation = row.find("td", class_="rel")
        date = row.find("td", class_="t_date")
        trade_code = row.find("td", class_="tran_code")
        shares = row.find("td", class_="sh")
        price = row.find("td", class_="pr")
        amount = row.find("td", class_="amt")

        if not symbol:
            continue
        
        
        try:
            clean_amount = float(amount.text.strip().replace(",", ""))
        except:
            clean_amount = None
        
        if trade_code:
            trade_type = trade_code.text.strip()
        else: trade_type = "Error"
    
        
        # print("\n--- ROW DEBUG ---")
        # print("Symbol:", symbol.text.strip())
        # print("Company:", company.text.strip())
        # print("Insider:", insider.text.strip())
        # print("Relation:", relation.text.strip())
        # print("Date:", date.text.strip())
        # print("Trade Code:", trade_code.text.strip())
        # print("Shares:", shares.text.strip())
        # print("Price:", price.text.strip())
        # print("Amount:", amount.text.strip())
        
        try:
            clean_price = float(price.text.strip().replace(",", ""))
            clean_shares = int(shares.text.strip().replace(",", ""))
        except:
            print("Numeric conversion failed.")
            continue

        data.append({
            "symbol": symbol.text.strip(),
            "company": company.text.strip(),
            "insider": insider.text.strip(),
            "relation": relation.text.strip(),
            "date": date.text.strip(),
            "price": clean_price,
            "trade_type": trade_type,
            "shares": clean_shares,
            "amount": clean_amount
        })

    print("\nScraping finished.")
    print(f"Parsed {len(data)} valid rows.")

    return data
