import requests
from bs4 import BeautifulSoup
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_photo(photo, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption
    })

def check_olx():
    url = "https://www.olx.com.pk/items/q-ac/lahore?filter=price_to_40000"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.find_all("a")

    for item in items:
        title = item.text.strip()
        link = item.get("href")

        if title and "AC" in title.upper():

            full_link = "https://www.olx.com.pk" + link

            parent = item.find_parent()

            price = ""
            description = ""
            image = ""

            if parent:
                # price try
                price_tag = parent.find(text=lambda x: x and "Rs" in x)
                if price_tag:
                    price = price_tag.strip()

                # image try
                img_tag = parent.find("img")
                if img_tag and img_tag.get("src"):
                    image = img_tag.get("src")

                # description try
                desc_tag = parent.find("span")
                if desc_tag:
                    description = desc_tag.text.strip()

            caption = f"""
🔥 Lahore AC Deal Found!

📌 {title}

💰 {price}

📝 {description}

🔗 Open: {full_link}
"""

            if image:
                send_photo(image, caption)
            else:
                # fallback text message
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    data={"chat_id": CHAT_ID, "text": caption}
                )

            break

while True:
    check_olx()
    time.sleep(300)
