 import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_amazon():
    # 아마존 반려견 용품 베스트셀러 주소
    url = "https://www.amazon.com/Best-Sellers-Pet-Supplies-Dog-Supplies/zgbs/pet-supplies/2975312011/"
    
    # 1. 아마존을 속이는 가짜 신분증 (User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        # 2. 접속 시도
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            products = []

            # 3. 아마존의 복잡한 태그에서 상품 찾기
            items = soup.find_all('div', {'id': 'gridItemRoot'})
            
            for item in items[:10]: # 상위 10개만 수집
                try:
                    name = item.find('div', class_='_cDEzb_p13n-sc-css-line-clamp-3_31q3p').text.strip()
                    price = item.find('span', class_='p13n-sc-price').text.strip()
                    products.append({"Product": name, "Price": price})
                except:
                    continue

            if products:
                pd.DataFrame(products).to_csv("amazon_data.csv", index=False, encoding='utf-8-sig')
                print("🎉 성공! 아마존 데이터를 가져왔습니다.")
            else:
                print("⚠️ 접속은 됐으나 데이터를 찾지 못했습니다. 태그 확인이 필요합니다.")
        
        elif response.status_code == 503:
            print("❌ 아마존이 로봇으로 감지하고 차단했습니다(503 에러).")
        else:
            print(f"❌ 접속 실패: {response.status_code}")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    scrape_amazon()
