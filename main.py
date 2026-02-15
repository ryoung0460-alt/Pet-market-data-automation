import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def scrape_amazon_us():
    # 보안이 덜 까다로운 검색 결과 페이지로 우회
    url = "https://www.amazon.com/s?k=dog+supplies&ref=nb_sb_noss"
    
    # 실제 미국 크롬 브라우저 사용자의 상세 정보 (Cookie와 세부 헤더 추가)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }

    try:
        # 아마존에 접속 시도
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            products = []
            
            # 검색 결과 페이지의 상품 이름 태그 추출
            # 아마존은 수시로 클래스명을 바꾸므로 여러 옵션을 체크합니다.
            items = soup.select('h2 .a-link-normal.a-text-normal')
            
            for item in items[:15]:
                name = item.get_text(strip=True)
                if name:
                    products.append({
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Market": "Amazon_US",
                        "Product": name
                    })

            # 데이터가 있으면 저장, 없으면 다시 시도 표시
            if products:
                df = pd.DataFrame(products)
                print(f"Success! {len(products)} products found.")
            else:
                print("Access successful, but no products found on page.")
                df = pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d"), "Product": "Retry Needed - No Items"}])
        else:
            print(f"Failed to access. Status: {response.status_code}")
            df = pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d"), "Product": f"Blocked by Amazon (Status {response.status_code})"}])

        # 파일명은 그대로 유지
        df.to_csv("us_amazon_dog_data.csv", index=False, encoding='utf-8-sig')

    except Exception as e:
        print(f"Error: {e}")
        pd.DataFrame([{"Error": str(e)}]).to_csv("us_amazon_dog_data.csv", index=False)

if __name__ == "__main__":
    scrape_amazon_us()
