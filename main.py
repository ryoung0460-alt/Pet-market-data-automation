import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def scrape_dog_market_final():
    # Using a simpler search URL to bypass bot detection
    url = "https://www.ebay.com/sch/i.html?_nkw=dog+vitamins+shampoo&_sacat=0"
    
    # Highly specific browser headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    }

    try:
        # Step 1: Request page
        response = requests.get(url, headers=headers, timeout=30)
        final_data = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            # Look for eBay item containers
            containers = soup.find_all("div", {"class": "s-item__info"})

            for container in containers:
                try:
                    title_box = container.find("div", {"class": "s-item__title"})
                    price_box = container.find("span", {"class": "s-item__price"})

                    if title_box and price_box:
                        name = title_box.get_text(strip=True).replace("New Listing", "")
                        price = price_box.get_text(strip=True)

                        # Exclude generic eBay ads
                        if "Shop on eBay" in name: continue

                        final_data.append({
                            "Date": datetime.now().strftime("%Y-%m-%d"),
                            "Category": "Health & Grooming",
                            "Item": name,
                            "Price": price
                        })
                except:
                    continue

        # Step 2: Save Results
        if final_data:
            df = pd.DataFrame(final_data[1:41]) # Take top 40 items
            df.to_csv("us_dog_market_data.csv", index=False, encoding='utf-8-sig')
            print(f"Success! Captured {len(df)} items.")
        else:
            # Last resort: If still blocked, create a detailed log
            print("Still blocked by eBay security.")
            pd.DataFrame([{"Status": "Security Blocked", "Time": datetime.now()}]).to_csv("us_dog_market_data.csv", index=False)

    except Exception as e:
        pd.DataFrame([{"Error": str(e)}]).to_csv("us_dog_market_data.csv", index=False)

if __name__ == "__main__":
    scrape_dog_market_final()
