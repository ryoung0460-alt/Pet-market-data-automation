import gspread
import os
import json
from datetime import datetime

def update_google_sheet():
    # 1. 깃허브 시크릿에서 JSON 키 로드
    creds_json = os.environ.get('GSPREAD_CREDENTIALS')
    if not creds_json:
        print("Error: GSPREAD_CREDENTIALS not found.")
        return

    try:
        creds_dict = json.loads(creds_json)
        # 2. 구글 시트 연결
        client = gspread.service_account_from_dict(creds_dict)
        # 시트 이름 확인
        spreadsheet = client.open("pet-collector") 
        sheet = spreadsheet.sheet1
    except Exception as e:
        print(f"Connection Error: {e}")
        return

    # 3. 데이터 준비
    current_date = datetime.now().strftime("%Y-%m-%d")
    products = [
        ["Zesty Paws Probiotics", "$26.97", "Supplements"],
        ["Burt's Bees Shampoo", "$10.89", "Shampoo"],
        ["Nutramax Dasuquin", "$65.99", "Supplements"],
        ["Greenies Dental Treats", "$34.98", "Treats"],
        ["PetHonesty Multivitamin", "$28.50", "Supplements"]
    ]
    
    # 데이터를 리스트 형태로 정렬
    new_rows = []
    for p in products:
        new_rows.append([current_date, "US_Pet_Market", p[2], p[0], p[1]])
    
    try:
        # 핵심 변경 사항: insert_rows를 사용하여 2행(헤더 바로 아래)에 삽입
        # 이렇게 하면 매일 최신 데이터가 가장 먼저 보입니다.
        sheet.insert_rows(new_rows, row=2)
        print(f"Success: {len(new_rows)} rows inserted at the top of 'pet-collector'!")
    except Exception as e:
        print(f"Write Error: {e}")

if __name__ == "__main__":
    update_google_sheet()
