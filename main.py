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

            # try to get more info from parent block
            parent = item.find_parent()

            description = ""
            price = ""

            if parent:
                desc_tag = parent.find("span")
                if desc_tag:
                    description = desc_tag.text.strip()

                price_tag = parent.find(text=lambda x: x and "Rs" in x)
                if price_tag:
                    price = price_tag.strip()

            msg = f"""
🔔 Lahore AC Found!

📌 Title: {title}

💰 Price: {price}

📝 Description: {description}

🔗 Link: {full_link}
"""

            send_msg(msg)
            break

while True:
    check_olx()
    time.sleep(300)
