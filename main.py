from venv import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.edge.service import Service
import telegram
import asyncio
import logging
import json
import keys


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, filename="main-py.log"
)


async def bot_message(input):
    bot = telegram.Bot(keys.token)
    async with bot:
        await bot.send_message(text=input, chat_id=376178155)


# My Phone chat ID: 376178155
# MY Bot Chat ID: 6174623243

chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(
    "/usr/lib/chromium-browser/chromedriver", options=chrome_options
)
logging.info("Opened Chromium Web-Browser")

# driver = webdriver.Firefox()
# driver = webdriver.Edge(
#     service=Service("/home/amsalem//Projects/DealBot/msedgedriver.exe")
# )

driver.get("https://t.me/s/McKenzie_Deals?q=zephyrus")
# msgs = driver.find_elements(
#     By.XPATH, value='//div[@class="tgme_widget_message_text js-message_text"]'
# )
msgs = driver.find_elements(By.CSS_SELECTOR, value="div.tgme_widget_message")

try:
    with open("zephyrus-ids.txt", "r", encoding="utf-16") as o:
        msgIds = json.load(o)
except Exception as e:
    logging.warning("Failed to open zephyrus-ids.txt. creating a new empty file")
    msgIds = []
    with open("zephyrus-ids.txt", "w+", encoding="utf-16") as f:
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
    with open("zephyrus-ids.txt", "w+", encoding="utf-16") as f:
        logging.info("Writing new ids to zephyrus-ids.txt")
        json.dump(newIds, f)
        f.close()
    with open("zephyrus.txt", "w+", encoding="utf-16") as f:
        logging.info("Writing new messages to zephyrus.txt")
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
