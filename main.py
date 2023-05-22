from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import telegram
import asyncio
import logging
import json
import keys
import searchQueries
from dataclasses import dataclass, field


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="./logs/DealBot.log",
)
# TO-DO: Create a class for deal search with channel name, and list of queries to check
# TO-DO: add support for script arguments with sys.argv for channel name and search terms
# TO-DO: Add logic to get only the last 5 deals from the output list got from selenium
# TO-DO: Add function when searching for terms with multiple words to replace spaces with +

CHATID = 376178155
# querys = ["zephyrus", "strix"]
# tChannel = "McKenzie_Deals"
# tChannel = "HTDeals"
# tChannel = "KSPcoil"

# Initialize searches classes
# kspSearch = Search(channel_name="KSPcoil", query_list=["rog laptop", "Rumba"])
# mckSearch = Search(channel_name="McKenzie_Deals", query_list=["zephyrus", "strix"])


# https://t.me/s/McKenzie_Deals?q=strix
# https://t.me/s/HTDeals?q=strix
# https://t.me/s/KSPcoil?q=strix+laptop


async def bot_message(input):
    bot = telegram.Bot(keys.token)
    async with bot:
        await bot.send_message(text=input, chat_id=CHATID)


querys = searchQueries.mckSearch.url
tChannel = searchQueries.mckSearch.channel_name

chrome_options = Options()
chrome_options.add_argument("--headless")

# For local docker selenium container on RPI4:
# driver = webdriver.Remote("http://localhost:4444/wd/hub", options=chrome_options)

# For selenium container on Z2Mini:
driver = webdriver.Remote("http://192.168.2.200:4444/wd/hub", options=chrome_options)

# For local on host selenium driver:
# driver = webdriver.Chrome(
#    service=Service("/usr/lib/chromium-browser/chromedriver"), options=chrome_options
# )
logging.info("Opened Chrome Web-Browser")

for query in querys:
    driver.get(f"https://t.me/s/{tChannel}?q={query}")
    msgs = driver.find_elements(By.CSS_SELECTOR, value="div.tgme_widget_message")

    try:
        with open(f"./data_lists/{query}-ids.txt", "r", encoding="utf-16") as o:
            msgIds = json.load(o)
    except Exception as e:
        logging.warning("Failed to open zephyrus-ids.txt. creating a new empty file")
        msgIds = []
        with open(f"./data_lists/{query}-ids.txt", "w+", encoding="utf-16") as f:
            f.write("")
            f.close()

    newIds = []
    newDeals = []
    for element in msgs:
        newIds.append(element.get_attribute("data-post"))

    if newIds == msgIds:
        logging.info("ID Lists are the same, No new messages")
        # driver.quit()
    else:
        with open(f"./data_lists/{query}-ids.txt", "w+", encoding="utf-16") as f:
            logging.info(f"Writing new ids to ./data_lists/{query}-ids.txt")
            json.dump(newIds, f)
            f.close()
        with open(f"./data_lists/{query}.txt", "w+", encoding="utf-16") as f:
            logging.info(f"Writing new messages to ./data_lists/{query}.txt")
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
            for id in newDeals[-5::]:
                for element in msgs:
                    if element.get_attribute("data-post") == id:
                        asyncio.run(bot_message(element.text))
    except Exception as e:
        print(e)
driver.quit()
logging.info("Web-Driver Closed")
