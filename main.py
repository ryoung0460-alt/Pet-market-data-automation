 import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def scrape_amazon_dog_data():
    # 아마존 반려견 용품 베스트셀러
    url = "https://www.amazon.com/Best-Sellers-Pet-Supplies-Dog-Supplies/zgbs/pet-supplies/2975312011/"
    
    # 보안 우회를 위한 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"접속 실패: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        products = []

        # 상품 리스트 찾기 (최신 아마존 태그 반영)
        items = soup.find_all('div', {'id': 'gridItemRoot'})
        
        for item in items:
            try:
                name = item.find('div', {'class': '_cDEzb_p13n-sc-css-line-clamp-3_31q3p'}).text.strip()
                price = item.find('span', {'class': 'p13n-sc-price'}).text.strip()
                
                products.append({
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Product": name,
                    "Price": price
                })
            except:
                continue

        if products:
            df = pd.DataFrame(products)
            filename = f"dog_market_data_{datetime.now().strftime('%Y_%m')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"성공! {filename} 파일이 생성되었습니다.")
        else:
            print("데이터를 찾지 못했습니다. 태그 확인이 필요합니다.")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    scrape_amazon_dog_data()
