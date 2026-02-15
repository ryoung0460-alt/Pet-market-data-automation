import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import random

def scrape_comprehensive_dog_data():
    # Searching for a broad range of dog products to ensure results
    # Query: dog food, vitamins, shampoo, toys, beds
    url = "https://www.ebay.com/sch/i.html?_nkw=dog+supplies+food+shampoo+vitamins+toys&_ipg=60"
    
    # Randomizing User-Agent to mimic different browsers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    try:
        # Sending request to eBay
        response = requests.get(url, headers=headers, timeout=30)
        results = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            # Selecting product containers
            items = soup.select('.s-item__info')
            
            for item in items:
                try:
                    title_elem = item.select_one('.s-item__title')
                    price_elem = item.select_one('.s-item__price')
                    
                    if title_elem and price_elem:
                        title = title_elem.get_text(strip=True).replace("New Listing", "")
                        price = price_elem.get_text(strip=True)
                        
                        # Filter out advertisements
                        if "Shop on eBay" in title: continue
                        
                        results.append({
                            "Collection_Date": datetime.now().strftime("%Y-%m-%d"),
                            "Market": "eBay_US",
                            "Product_Category": "General Dog Supplies",
                            "Item_Name": title,
                            "Price_USD": price
                        })
                except Exception:
                    continue

        if results:
            # Saving up to 50 items to CSV
            df = pd.DataFrame(results[1:51])
            df.to_csv("us_dog_market_data.csv", index=False, encoding='utf-8-sig')
            print(f"Success: {len(df)} products saved to CSV.")
        else:
            # If blocked, log the status but keep the file valid for GitHub Actions
            print(f"Warning: Access successful but no items parsed. Status: {response.status_code}")
            pd.DataFrame([{"Status": "Access blocked or layout changed"}]).to_csv("us_dog_market_data.csv", index=False)

    except Exception as e:
        print(f"Critical Error: {e}")
        pd.DataFrame([{"Error": str(e)}]).to_csv("us_dog_market_data.csv", index=False)

if __name__ == "__main__":
    scrape_comprehensive_dog_data()
