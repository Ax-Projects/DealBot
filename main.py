from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import telegram
import asyncio
import logging
import json, os
import keys
import searchQueries

# from selenium.webdriver.chrome.service import Service


CHATID = 376178155
DATAFOLD = "./data_lists"
LOGSFOLD = "./logs"

## Creating folders
os.makedirs(DATAFOLD, exist_ok=True)
os.makedirs(LOGSFOLD, exist_ok=True)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="./logs/DealBot.log",
)

# TODO: move the search queries and channels to a separate file and import them like Key.py file
# TO-DO: Create a class for deal search with channel name, and list of queries to check -- DONE
# TODO: add support for script arguments with sys.argv for channel name and search terms
# TO-DO: Add logic to get only the last 4 deals from the output list got from selenium  -- DONE
# TO-DO: Add function when searching for terms with multiple words to replace spaces with +  -- DONE
# TODO: update the readme file


def open_deals_file(filename):
    try:
        with open(f"./data_lists/{filename}-ids.txt", "r", encoding="utf-16") as o:
            return json.load(o)
    except Exception as e:
        logging.warning(e)
        logging.warning(f"Failed to open {filename}-ids.txt. creating a new empty file")
        with open(f"./data_lists/{filename}-ids.txt", "w+", encoding="utf-16") as f:
            f.write("[]")
            f.close()
        return []


def get_web_msg(url):
    driver.get(url)
    msgs = driver.find_elements(By.CSS_SELECTOR, value="div.tgme_widget_message")
    return msgs


def get_chName(channel):
    return channel.channel_name


def get_chUrl(channel):
    return channel.url


async def bot_message(input):
    bot = telegram.Bot(keys.token)
    async with bot:
        await bot.send_message(text=input, chat_id=CHATID)


## Creating a list as long as number of searches in SearchesList.json file
file = f"{os.getcwd()}/SearchesList.json"
with open(file) as f:
    searchList: dict = json.load(f)

# searches = []
# for i in range(len(searchList)):
#     search = f"s{i}"  ## Each element in the searches list is "s" + number, depend on the number of searches
#     globals()[search] = None
#     searches.append(search)


# # Initialize searches classes for each variable in the searches list
# for i, k in zip(searches, searchList):
#     x = searchQueries.Search(k, searchList[k])
#     globals()[i] = x


## Defining Chrome options for headless run in selenium which removes dependency on connection to a monitor
chrome_options = Options()
chrome_options.add_argument("--headless")

# # For local docker selenium container on RPI4:
driver = webdriver.Remote("http://10.0.0.180:4444/wd/hub", options=chrome_options)
# # driver = webdriver.Remote("http://localhost:4444/")

# For selenium container on Z2Mini:
# driver = webdriver.Remote("http://10.147.20.195:4444/wd/hub", options=chrome_options)

# For local on host selenium driver:
# driver = webdriver.Chrome(
#    service=Service("/usr/lib/chromium-browser/chromedriver"), options=chrome_options
# )
# logging.info("Opened Chrome Web-Browser")

for e in searchList.keys():
    c = searchQueries.Search(e, searchList[e])
    cName = get_chName(c)
    queries = get_chUrl(c)
    # for item in queries:
    #     logging.info(f"Querying url: {item}")
    #     print("quering: ", item)
    for i in range(len(queries)):
        driver.start_client()
        q = (
            c.query_list[i].strip().replace(" ", "-")
        )  ## removing white spaces from search terms
        fnm = f"{cName}.{q}"
        print("filename for current query: ", fnm)
        logging.info(f"Querying url: {queries[i]}")
        print("quering: ", queries[i])
        msgs = []
        msgs = get_web_msg(queries[i])
        msgIds = open_deals_file(fnm)
        newIds = []
        for element in msgs:
            newIds.append(element.get_attribute("data-post"))

        # print(any(map(lambda x: x in newIds, msgIds)))
        difference = list(set(newIds) - set(msgIds))
        if len(difference) == 0:
            print(f"{fnm}: No new deals")
            logging.info("ID Lists are the same, No new messages")
            driver.stop_client()
        else:
            newDeals = []
            with open(f"./data_lists/{fnm}-ids.txt", "w+", encoding="utf-16") as f:
                logging.info(f"Writing new ids to ./data_lists/{fnm}-ids.txt")
                json.dump(newIds, f)
                f.close()
            #### for debugging messages content
            # with open(f"./data_lists/{fnm}.txt", "w+", encoding="utf-16") as f:
            #     logging.info(f"Writing new messages to ./data_lists/{fnm}.txt")
            #     for element in msgs:
            #         f.write(element.text)
            #     f.close()
            for i in range(len(newIds)):
                if newIds[i] not in msgIds:
                    newDeals.append(newIds[i])
            print(f"Closing webDriver after fethcing new deal of {fnm}")
            driver.stop_client()

            try:
                if len(newDeals) > 0:
                    logging.info("New Deals found! Sending Messages in Telegram Bot")
                    asyncio.run(bot_message("A New Deal was found!\n"))
                    for id in sorted(newDeals)[-4::]:
                        for element in msgs:
                            if element.get_attribute("data-post") == id:
                                asyncio.run(bot_message(element.text))
            except Exception as e:
                print(e)
driver.quit()

logging.info("Web-Driver Closed")
