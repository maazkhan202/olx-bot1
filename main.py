import requests
import time
import os

BOT_TOKEN = os.getenv("8270357259:AAHS17HK9LAh3aveYQaQsIzGprFHX91LjcE")
CHAT_ID = os.getenv("7605836389")

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def check_olx():
    url = "https://www.olx.com.pk/items/q-ac?filter=price_to_40000"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)

    if "AC" in r.text.upper():
        send_msg("🔔 New AC found under 40k!")

while True:
    check_olx()
    time.sleep(300)