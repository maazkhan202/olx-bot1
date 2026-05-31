import requests
from bs4 import BeautifulSoup
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def send_photo(photo, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption
    })

def check_olx():
    url = "https://www.olx.com.pk/items/q-air-conditioner/lahore?filter=price_to_40000"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.find_all("a")

    for item in items:
        title = item.text.strip()
        link = item.get("href")

        if not title or not link:
            continue

        title_up = title.upper()

        # ✅ ONLY REAL AC ADS
        if not any(k in title_up for k in ["AIR CONDITIONER", "AC", "SPLIT AC"]):
            continue

        # ❌ BLOCK FAKE / ACCESSORIES ADS
        if any(b in title_up for b in ["ACCESSORY", "MOBILE", "PHONE", "COVER", "HOLDER"]):
            continue

        full_link = "https://www.olx.com.pk" + link

        parent = item.find_parent()

        price = ""
        image = ""

        if parent:
            price_tag = parent.find(text=lambda x: x and "Rs" in x)
            if price_tag:
                price = price_tag.strip()

            img_tag = parent.find("img")
            if img_tag and img_tag.get("src"):
                image = img_tag.get("src")

        caption = f"""
🔥 Lahore AC Deal Found!

📌 {title}

💰 {price}

🔗 {full_link}
"""

        if image:
            send_photo(image, caption)
        else:
            send_msg(caption)

        break

while True:
    check_olx()
    time.sleep(300)
