import requests
from bs4 import BeautifulSoup
import time
import hashlib

# Telegram Bot API URL and your bot token
TELEGRAM_API_URL = "https://api.telegram.org/bot"
BOT_TOKEN = "6505638593:AAEsWBviZ0dpzeyiCYk-Ga4y33RX0BOnzJY"
CHAT_ID = "5119888403"

# Function to send message through Telegram bot
def send_telegram_message(message):
    send_url = f"{TELEGRAM_API_URL}{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
    }
    try:
        response = requests.post(send_url, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

# Function to fetch and hash the content of interest
def fetch_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select_one('section.latest-added').encode('utf-8')
        # Hash the content for easy comparison
        content_hash = hashlib.md5(content).hexdigest()
        return content_hash
    except Exception as e:
        print(f"Error fetching the content: {e}")
        return None

# Function to periodically check the website
def monitor_website(url, interval=300):
    print("Starting the monitoring process...")
    last_hash = None
    while True:
        current_hash = fetch_content(url)
        if current_hash is None:
            print("Failed to fetch the content. Trying again next cycle.")
        elif last_hash is not None and current_hash != last_hash:
            message = "Change detected on https://anonymsms.com/! Check out the latest changes."
            send_telegram_message(message)
            print("Change detected! Notification sent.")
        else:
            print("No change detected.")
        last_hash = current_hash
        time.sleep(interval)

# URL to monitor
url = 'https://bac96839-6a93-427d-b4f7-9af1cc638e49-00-7z585xalbq4s.pike.replit.dev/'

# Start monitoring with a check every 5 minutes (300 seconds)
monitor_website(url, 10)
