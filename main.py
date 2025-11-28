import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ---------- Telegram Settings ----------
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

KEYWORDS = ["help", "assistance", "cashphrase"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)


# ---------- Chrome Setup ----------
chrome_options = Options()

# Use your real Chrome profile
chrome_options.add_argument(
    r"user-data-dir=C:\Users\user\AppData\Local\Google\Chrome\User Data"
)
chrome_options.add_argument("profile-directory=Profile 3")

# Optional: use real Chrome
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

driver = webdriver.Chrome(options=chrome_options)

# ---------- Pages to Monitor ----------
URLS = [
    "https://yourcompanydashboard.com/page1",
    "https://yourcompanydashboard.com/page2"
]

# Open tabs
if len(URLS) > 0:
    driver.get(URLS[0])
    for url in URLS[1:]:
        driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(1)

print("🚀 Monitoring started. Waiting for keywords...")


def check_page(tab_index):
    html = driver.page_source.lower()
    found = False

    for word in KEYWORDS:
        if word.lower() in html:
            send_telegram(f"⚠️ Keyword detected in Tab {tab_index + 1}: '{word}'")
            print(f"[ALERT] Keyword detected: {word}")
            found = True

    return found


# ---------- Monitoring Loop ----------
while True:
    for index, tab in enumerate(driver.window_handles):
        driver.switch_to.window(tab)
        print(f"Checking tab {index + 1}...")
        time.sleep(1)

        check_page(index)

    time.sleep(5)  # adjust scanning speed
