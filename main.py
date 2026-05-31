import requests
from bs4 import BeautifulSoup
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def check_olx():
    url = "https://www.olx.com.pk/items/q-ac?filter=price_to_40000"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.find_all("a")

    for item in items:
        title = item.text.strip()
        link = item.get("href")

        if title and "AC" in title.upper():
            full_link = "https://www.olx.com.pk" + link
            msg = f"🔔 New AC Found!\n\n{title}\n{full_link}"
            send_msg(msg)
            break

while True:
    check_olx()
    time.sleep(300)
