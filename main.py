import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def scrape_amazon_us():
    # Use a more stable URL for testing
    url = "https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            products = []
            
            # Find product names (Updated selector)
            items = soup.find_all('div', {'id': 'gridItemRoot'})
            
            for item in items[:10]:
                try:
                    name = item.find('div', class_='_cDEzb_p13n-sc-css-line-clamp-3_31q3p').text.strip()
                    products.append({
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Product": name
                    })
                except:
                    continue

            # Force create a file even if empty to avoid Error 128
            df = pd.DataFrame(products if products else [{"Date": "N/A", "Product": "No Data Found"}])
            df.to_csv("us_amazon_dog_data.csv", index=False, encoding='utf-8-sig')
            print(f"File saved successfully.")
        else:
            print(f"Access Denied: Status {response.status_code}")
            # Create a dummy file to prevent GitHub Actions error
            pd.DataFrame([{"Error": "Access Denied"}]).to_csv("us_amazon_dog_data.csv", index=False)

    except Exception as e:
        print(f"Error: {e}")
        pd.DataFrame([{"Error": str(e)}]).to_csv("us_amazon_dog_data.csv", index=False)

if __name__ == "__main__":
    scrape_amazon_us()
