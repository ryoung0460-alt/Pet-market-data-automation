import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def scrape_ebay_dog_market():
    # Target: eBay US search results for comprehensive dog supplies
    # Includes: Food, Toys, Supplements, Shampoo, etc.
    url = "https://www.ebay.com/sch/i.html?_nkw=dog+supplies+food+supplements+shampoo"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        product_list = []
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.select('.s-item__wrapper')
            
            for item in items:
                try:
                    title_elem = item.select_one('.s-item__title')
                    if not title_elem: continue
                    
                    # Clean title: Remove "New Listing" prefix
                    raw_title = title_elem.get_text(strip=True)
                    clean_title = raw_title.replace("New Listing", "").strip()
                    
                    # Filter out non-product entries
                    if "Shop on eBay" in clean_title: continue
                    
                    price_elem = item.select_one('.s-item__price')
                    price = price_elem.get_text(strip=True) if price_elem else "N/A"
                    
                    if clean_title:
                        product_list.append({
                            "Date": datetime.now().strftime("%Y-%m-%d"),
                            "Source": "eBay_US",
                            "Product_Name": clean_title,
                            "Price": price
                        })
                except Exception:
                    continue

        if product_list:
            # Saving data to CSV (excluding the first dummy item if necessary)
            df = pd.DataFrame(product_list[1:31]) # Collect top 30 items
            # Using the filename synchronized with your GitHub Actions setting
            df.to_csv("us_dog_market_data.csv", index=False, encoding='utf-8-sig')
            print(f"Success: {len(df)} items collected and saved to CSV.")
        else:
            print("No products found. Creating an empty report.")
            pd.DataFrame([{"Status": "No data available"}]).to_csv("us_dog_market_data.csv", index=False)

    except Exception as e:
        print(f"Error occurred: {e}")
        error_df = pd.DataFrame([{"Error_Log": str(e)}])
        error_df.to_csv("us_dog_market_data.csv", index=False)

if __name__ == "__main__":
    scrape_ebay_dog_market()
