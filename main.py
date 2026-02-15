import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_ebay_us():
    # eBay US Dog Supplies Best Sellers
    url = "https://www.ebay.com/b/Dog-Supplies/1281/bn_1865464"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        products = []
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # eBay items usually sit in 's-item__info' or 'b-tile'
            items = soup.select('.s-item__info')
            
            for item in items:
                try:
                    # Get product title
                    name_elem = item.select_one('.s-item__title')
                    if not name_elem: continue
                    name = name_elem.get_text(strip=True)
                    
                    # Skip generic "Shop on eBay" titles
                    if "Shop on eBay" in name: continue
                    
                    # Get price
                    price_elem = item.select_one('.s-item__price')
                    price = price_elem.get_text(strip=True) if price_elem else "N/A"
                    
                    products.append({
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Market": "eBay_US",
                        "Product": name,
                        "Price": price
                    })
                except:
                    continue

        if products:
            # Save top 20 items
            df = pd.DataFrame(products[:20])
            df.to_csv("us_dog_market_data.csv", index=False, encoding='utf-8-sig')
            print(f"Success: {len(products[:20])} items collected from eBay.")
        else:
            # Create a fallback file if failed
            print("Access Denied or No Items Found")
            pd.DataFrame([{"Status": "Failed to collect from eBay"}]).to_csv("us_dog_market_data.csv", index=False)

    except Exception as e:
        print(f"Error: {e}")
        pd.DataFrame([{"Error": str(e)}]).to_csv("us_dog_market_data.csv", index=False)

if __name__ == "__main__":
    scrape_ebay_us()
