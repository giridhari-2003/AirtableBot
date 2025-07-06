import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}"
}

def get_all_rows():
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["records"]

def get_today_new_records():
    today = datetime.now(timezone.utc).date()
    records = get_all_rows()
    new_records = []

    for rec in records:
        created_time = rec.get("createdTime")
        if created_time:
            created_date = datetime.fromisoformat(created_time[:-1]).date()
            if created_date == today:
                new_records.append(rec)
    
    return new_records
