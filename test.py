import requests
import os
from dotenv import load_dotenv

load_dotenv()

# TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = "7086358521:AAGqAG_EMO3OiOG5rOqk6XkbWG33PVAlAIk"

def get_updates():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    resp = requests.get(url)
    print(resp.json())

if __name__ == "__main__":
    get_updates()
