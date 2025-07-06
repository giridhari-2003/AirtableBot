import time
import schedule
import threading
from airtable_utils import get_all_rows, get_today_new_records
from telegram_handler import send_telegram_message
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
print(f"🔑 Using Telegram Bot Token:   {BOT_TOKEN}")

def send_row_count():
    records = get_all_rows()
    msg = f"🔄 Airtable Sync Update:\nTotal records: {len(records)}"
    send_telegram_message(msg)

# def check_for_user_message():
#     url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
#     response = requests.get(url)
#     updates = response.json().get("result", [])
#     for update in updates:
#         message_text = update.get("message", {}).get("text", "").lower()
#         chat_id = update.get("message", {}).get("chat", {}).get("id")
#         if message_text == "new registration":
#             new_records = get_today_new_records()
#             if new_records:
#                 msg = f"🆕 New registrations today: {len(new_records)}\n"
#                 for rec in new_records:
#                     fields = rec["fields"]
#                     name = fields.get("Name", "No Name")
#                     msg += f"• {name}\n"
#             else:
#                 msg = "No new registrations today."
#             send_telegram_message(msg)

# def run_polling():
#     while True:
#         check_for_user_message()
#         time.sleep(15)

def check_for_user_message(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    response = requests.get(url)
    updates = response.json().get("result", [])
    return updates

def run_polling():
    last_update_id = None

    while True:
        updates = check_for_user_message(offset=last_update_id)
        for update in updates:
            update_id = update["update_id"]
            last_update_id = update_id + 1  # So we skip this one next time

            message = update.get("message", {})
            message_text = message.get("text", "").lower()
            chat_id = message.get("chat", {}).get("id")

            if message_text == "new registration":
                new_records = get_today_new_records()
                if new_records:
                    msg = f"🆕 New registrations today: {len(new_records)}\n"
                    for rec in new_records:
                        fields = rec["fields"]
                        name = fields.get("Name", "No Name")
                        msg += f"• {name}\n"
                else:
                    msg = "No new registrations today."

                send_telegram_message(msg)

        time.sleep(2)


# Schedule the job every 30 mins
schedule.every(30).minutes.do(send_row_count)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == "__main__":
    print("📡 Starting Airtable Telegram Monitor")
    threading.Thread(target=run_scheduler).start()
    threading.Thread(target=run_polling).start()
