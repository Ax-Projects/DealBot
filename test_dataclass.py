from dataclasses import dataclass, field
from re import T


@dataclass
class Search:
    channel_name: str
    query_list: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.query_list) > 1:
            _urls = []
            for n in range(len(self.query_list)):
                _qry = self.query_list[n].strip().replace(" ", "+")
                _urls.append(f"https://t.me/s/{self.channel_name}?q={_qry}")
            self.url = _urls
        elif len(self.query_list) == 1:
            _qry = self.query_list[0].strip().replace(" ", "+")
            self.url = [f"https://t.me/s/{self.channel_name}?q={_qry}"]


def validateSearch(search):
    if not (search.channel_name and search.query_list):
        return False
    else:
        return True


kspSearch = Search(channel_name="KSPcoil", query_list=["rog laptop", "Rumba"])
mckSearch = Search(channel_name="McKenzie_Deals", query_list=["zephyrus", "strix"])
htdSearch = Search("HTDeals", ["מסך חיצוני", "steelseries"])


def get_chName(channel):
    return channel.channel_name


def get_chUrl(channel):
    return channel.url


tch = [kspSearch, mckSearch, htdSearch]
for c in tch:
    queries = get_chUrl(c)
    cName = get_chName(c)
    for item in queries:
        print(item)
        # driver.get(item)
        # msgs = driver.find_elements(
        #     By.CSS_SELECTOR, value="div.tgme_widget_message"
        # )
        for i in range(len(queries)):
            q = c.query_list[i].strip().replace(" ", "+")
            fnm = f"{cName}.{q}"
            print(fnm)
# querys = [mckSearch.url, htdSearch.url, kspSearch.url]
# tChannel = mckSearch.channel_name

# for index in range(len(queries)):
#     for item in queries[index]:
#         print(item)

# print(validateSearch(kspSearch))
# print(validateSearch(mckSearch))
# print(validateSearch(htdSearch))
# print(kspSearch.url)
# print(mckSearch.url)
# print(htdSearch.url)
# print(htdSearch.channel_name)
# print(testSearch.url)
