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

# from dataclasses import dataclass, field


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


def open_deals_file(filename):
    try:
        with open(f"./data_lists/{filename}-ids.txt", "r", encoding="utf-16") as o:
            return json.load(o)
    except Exception as e:
        logging.warning(e)
        logging.warning(f"Failed to open {filename}-ids.txt. creating a new empty file")
        with open(f"./data_lists/{filename}-ids.txt", "w+", encoding="utf-16") as f:
            f.write("")
            f.close()
        return []


async def bot_message(input):
    bot = telegram.Bot(keys.token)
    async with bot:
        await bot.send_message(text=input, chat_id=CHATID)


# Initialize searches classes
kspSearch = searchQueries.Search(
    channel_name="KSPcoil", query_list=["rog laptop", "Rumba"]
)
mckSearch = searchQueries.Search(
    channel_name="McKenzie_Deals", query_list=["zephyrus", "strix"]
)
htdSearch = searchQueries.Search("HTDeals", ["מסך חיצוני", "steelseries"])

## Here are the queries and channels lists ##
querys = [mckSearch.url, htdSearch.url, kspSearch.url]
tChannels = [mckSearch.channel_name, htdSearch.channel_name, kspSearch.channel_name]

chrome_options = Options()
chrome_options.add_argument("--headless")

# For local docker selenium container on RPI4:
# driver = webdriver.Remote("http://localhost:4444/wd/hub", options=chrome_options)

# For selenium container on Z2Mini:
driver = webdriver.Remote("http://localhost:4444/wd/hub", options=chrome_options)

# For local on host selenium driver:
# driver = webdriver.Chrome(
#    service=Service("/usr/lib/chromium-browser/chromedriver"), options=chrome_options
# )
logging.info("Opened Chrome Web-Browser")

for chnl in tChannels:
    open_deals_file(chnl)

for index in range(len(tChannels)):
    for item in querys[index]:
        driver.get(item)
        msgs = driver.find_elements(By.CSS_SELECTOR, value="div.tgme_widget_message")

    msgIds = open_deals_file(tChannels[index])
    newIds = []
    newDeals = []
    for element in msgs:
        newIds.append(element.get_attribute("data-post"))

    if newIds in msgIds:
        logging.info("ID Lists are the same, No new messages")
        # driver.quit()
    else:
        with open(
            f"./data_lists/{tChannels[index]}-ids.txt", "w+", encoding="utf-16"
        ) as f:
            logging.info(f"Writing new ids to ./data_lists/{tChannels[index]}-ids.txt")
            json.dump(newIds, f)
            f.close()
        with open(f"./data_lists/{tChannels[index]}.txt", "w+", encoding="utf-16") as f:
            logging.info(f"Writing new messages to ./data_lists/{tChannels[index]}.txt")
            for element in msgs:
                f.write(element.text)
            f.close()
        for i in range(len(newIds)):
            if newIds[i] not in msgIds:
                newDeals.append(newIds[i])

    try:
        if len(newDeals) > 0:
            logging.info("New Deals found! Sending Messages in Telegram Bot")
            # asyncio.run(bot_message("A New Deal was found!\n"))
            for id in newDeals[-5::]:
                for element in msgs:
                    if element.get_attribute("data-post") == id:
                        print(element.text)
                        # asyncio.run(bot_message(element.text))
    except Exception as e:
        print(e)
driver.quit()
logging.info("Web-Driver Closed")
