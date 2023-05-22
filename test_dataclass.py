from dataclasses import dataclass, field


querys = ["zephyrus", "strix"]
# tChannel = "McKenzie_Deals"
# tChannel = "HTDeals"
tChannel = "KSPcoil"


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
            self.url = f"https://t.me/s/{self.channel_name}?q={_qry}"


def validateSearch(search):
    if not (search.channel_name and search.query_list):
        return False
    else:
        return True


try:
    testSearch = Search(channel_name="testChannel")
except:
    pass
kspSearch = Search(channel_name="KSPcoil", query_list=["rog laptop", "Rumba"])
mckSearch = Search(channel_name="McKenzie_Deals", query_list=["zephyrus"])

print(validateSearch(kspSearch))
print(validateSearch(mckSearch))
print(validateSearch(testSearch))
print(kspSearch.url)
print(mckSearch.url)
# print(testSearch.url)
