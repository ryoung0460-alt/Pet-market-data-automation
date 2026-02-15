 import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_ebay_dog_items():
    # eBay 미국 반려견 용품 베스트셀러 검색 결과
    url = "https://www.ebay.com/b/Dog-Supplies/1281/bn_1865464"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        products = []

        # eBay 상품 리스트 태그 (최신 구조 반영)
        items = soup.find_all('li', class_='s-item')
        
        for item in items[1:16]: # 첫 번째 아이템은 보통 광고라 생략하고 15개 수집
            try:
                name = item.find('div', class_='s-item__title').text.strip()
                price = item.find('span', class_='s-item__price').text.strip()
                
                products.append({
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Market": "eBay_US",
                    "Product": name,
                    "Price": price
                })
            except:
                continue

        if products:
            df = pd.DataFrame(products)
            df.to_csv("us_dog_market_data.csv", index=False, encoding='utf-8-sig')
            print("🎉 Success: US Market data collected from eBay!")
        else:
            print("⚠️ Could not find items. Checking tags...")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrape_ebay_dog_items()
