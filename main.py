from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import telegram
import asyncio
import logging
import json
import keys


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, filename="main-py.log"
)

CHATID = 376178155
query = "zephyrus"
tChannel = "McKenzie_Deals"

async def bot_message(input):
    bot = telegram.Bot(keys.token)
    async with bot:
        await bot.send_message(text=input, chat_id=CHATID)

chrome_options = Options()
chrome_options.add_argument("--headless")
## EDIT THIS DRIVER PATH TO THE LOCATION OF YOUR CHROME DRIVER EXE. 
## If the Chrome driver already included in PATH, just remove the path string written here and leave it as webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome(
    "/usr/lib/chromium-browser/chromedriver", options=chrome_options
)
logging.info("Opened Chromium Web-Browser")


driver.get(f"https://t.me/s/{tChannel}?q={query}")
msgs = driver.find_elements(By.CSS_SELECTOR, value="div.tgme_widget_message")

try:
    with open(f"{query}-ids.txt", "r", encoding="utf-16") as o:
        msgIds = json.load(o)
except Exception as e:
    logging.warning("Failed to open zephyrus-ids.txt. creating a new empty file")
    msgIds = []
    with open(f"{query}-ids.txt", "w+", encoding="utf-16") as f:
        f.write("")
        f.close()

newIds = []
newDeals = []
for element in msgs:
    newIds.append(element.get_attribute("data-post"))

if newIds == msgIds:
    logging.info("ID Lists are the same, No new messages")
    driver.quit()
else:
    with open(f"{query}-ids.txt", "w+", encoding="utf-16") as f:
        logging.info(f"Writing new ids to {query}-ids.txt")
        json.dump(newIds, f)
        f.close()
    with open(f"{query}.txt", "w+", encoding="utf-16") as f:
        logging.info(f"Writing new messages to {query}.txt")
        for element in msgs:
            f.write(element.text)
        f.close()
    for i in range(len(newIds)):
        if newIds[i] not in msgIds:
            newDeals.append(newIds[i])

try:
    if len(newDeals) > 0:
        logging.info("New Deals found! Sending Messages in Telegram Bot")
        asyncio.run(bot_message("A New Deal was found!\n"))
        for id in newDeals:
            for element in msgs:
                if element.get_attribute("data-post") == id:
                    asyncio.run(bot_message(element.text))
except Exception as e:
    print(e)

driver.quit()
logging.info("Web-Driver Closed")
