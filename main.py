 import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_amazon_dog_data():
    url = "https://www.amazon.com/Best-Sellers-Pet-Supplies-Dog-Supplies/zgbs/pet-supplies/2975312011/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        # 데이터 수집 로직... (생략 가능, 위에서 드린 전체 코드를 쓰세요)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_amazon_dog_data()
