import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_amazon_dog_data():
    # 미국 아마존 반려견 용품 베스트셀러 주소
    url = "https://www.amazon.com/Best-Sellers-Pet-Supplies-Dog-Supplies/zgbs/pet-supplies/2975312011/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        products = []

        # 아마존 상품 리스트 추출 (태그는 주기적으로 변할 수 있음)
        items = soup.select('.p13n-gridRow .zg-grid-general-faceout')
        for item in items:
            try:
                name = item.select_one('.p13n-sc-truncate').text.strip()
                price = item.select_one('.p13n-sc-price').text.strip() if item.select_one('.p13n-sc-price') else "N/A"
                rating = item.select_one('.a-icon-alt').text.strip() if item.select_one('.a-icon-alt') else "N/A"
                
                products.append({
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Product": name,
                    "Price": price,
                    "Rating": rating
                })
            except: continue

        if products:
            df = pd.DataFrame(products)
            # 검로드 판매용 엑셀 파일명 생성
            filename = f"dog_market_data_{datetime.now().strftime('%Y_%m')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Success! {filename} created.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_amazon_dog_data()
