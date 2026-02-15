import gspread
import os
import json
from datetime import datetime

def update_google_sheet():
    # 1. Load Credentials from GitHub Secrets
    creds_json = os.environ.get('GSPREAD_CREDENTIALS')
    if not creds_json:
        print("Error: GSPREAD_CREDENTIALS not found in environment.")
        return

    try:
        creds_dict = json.loads(creds_json)
        # 2. Connect to Google Sheets
        client = gspread.service_account_from_dict(creds_dict)
        
        # Open by name: Must match your file name 'pet-collector' exactly
        spreadsheet = client.open("pet-collector") 
        
        # Select the first tab (Worksheet) regardless of its name (시트1 or Sheet1)
        sheet = spreadsheet.get_worksheet(0)
    except Exception as e:
        print(f"Connection/Auth Error: {e}")
        return

    # 3. Prepare Data
    current_date = datetime.now().strftime("%Y-%m-%d")
    products = [
        ["Zesty Paws Probiotics", "$26.97", "Supplements"],
        ["Burt's Bees Shampoo", "$10.89", "Shampoo"],
        ["Nutramax Dasuquin", "$65.99", "Supplements"],
        ["Greenies Dental Treats", "$34.98", "Treats"],
        ["PetHonesty Multivitamin", "$28.50", "Supplements"]
    ]
    
    new_rows = []
    for p in products:
        # Format: Date | Market | Category | Product Name | Price
        new_rows.append([current_date, "US_Pet_Market", p[2], p[0], p[1]])
    
    try:
        # 4. Insert rows at the top (Row 2, below header)
        sheet.insert_rows(new_rows, row=2)
        print(f"Success: {len(new_rows)} rows inserted!")
    except Exception as e:
        print(f"Data Write Error: {e}")

if __name__ == "__main__":
    update_google_sheet()
