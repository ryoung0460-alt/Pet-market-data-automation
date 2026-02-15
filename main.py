import gspread
import os
import json
from datetime import datetime

def update_google_sheet():
    # 1. Access Credentials
    creds_json = os.environ.get('GSPREAD_CREDENTIALS')
    if not creds_json:
        print("Error: Credentials missing.")
        return

    try:
        creds_dict = json.loads(creds_json)
        client = gspread.service_account_from_dict(creds_dict)
        
        # 2. Open Spreadsheet (Must match your file name exactly)
        # We use 'Pet-collector' as you confirmed.
        spreadsheet = client.open("Pet-collector") 
        
        # 3. Select the very first tab regardless of its name ('Pet-collector' or '시트1')
        sheet = spreadsheet.get_worksheet(0)
        
        print(f"Connected to sheet: {spreadsheet.title}")
    except Exception as e:
        print(f"Auth or Connection Error: {e}")
        return

    # 4. Data to insert
    current_date = datetime.now().strftime("%Y-%m-%d")
    data_to_insert = [
        [current_date, "US_Pet_Market", "Supplements", "Zesty Paws Probiotics", "$26.97"],
        [current_date, "US_Pet_Market", "Shampoo", "Burt's Bees Shampoo", "$10.89"],
        [current_date, "US_Pet_Market", "Supplements", "Nutramax Dasuquin", "$65.99"],
        [current_date, "US_Pet_Market", "Treats", "Greenies Dental Treats", "$34.98"],
        [current_date, "US_Pet_Market", "Supplements", "PetHonesty Multivitamin", "$28.50"]
    ]
    
    try:
        # 5. Insert right below the header (Row 2)
        sheet.insert_rows(data_to_insert, row=2)
        print("Success: Data successfully pushed to Google Sheets!")
    except Exception as e:
        print(f"Write Error: {e}")

if __name__ == "__main__":
    update_google_sheet()
