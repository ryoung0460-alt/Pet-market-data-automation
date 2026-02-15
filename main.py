 import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_amazon_us():
    url = "https://www.amazon.com/Best-Sellers-Pet-Supplies-Dog-Supplies/zgbs/pet-supplies/2975312011/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"Status Error: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        products = []
        items = soup.select('div#gridItemRoot')

        for item in items[:20]:
            try:
                name_elem = item.select_one('.p13n-sc-truncate')
                name = name_elem.text.strip() if name_elem else "N/A"
                
                price_elem = item.select_one('.p13n-sc-price')
                price = price_elem.text.strip() if price_elem else "N/A"

                if name != "N/A":
                    products.append({
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Market": "Amazon_US",
                        "Product": name,
                        "Price": price
                    })
            except Exception:
                continue

        if products:
            df = pd.DataFrame(products)
            df.to_csv("us_amazon_dog_data.csv", index=False, encoding='utf-8-sig')
            print(f"Success: {len(products)} items saved.")
        else:
            print("No items found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_amazon_us()
