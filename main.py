 import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_data():
    url = "https://www.amazon.com/Best-Sellers-Pet-Supplies-Dog-Supplies/zgbs/pet-supplies/2975312011/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        items = soup.select('.p13n-gridRow .zg-grid-general-faceout')
        
        data = []
        for item in items[:10]: # 상위 10개만 테스트
            name = item.select_one('.p13n-sc-truncate').text.strip()
            price = item.select_one('.p13n-sc-price').text.strip() if item.select_one('.p13n-sc-price') else "N/A"
            data.append({"Date": datetime.now().strftime("%Y-%m-%d"), "Product": name, "Price": price})
        
        if data:
            pd.DataFrame(data).to_csv("dog_market_data.csv", index=False, encoding='utf-8-sig')
            print("Success: File created")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_data()
