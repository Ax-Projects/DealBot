from dataclasses import dataclass, field


@dataclass
class Search:
    channel_name: str
    query_list: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.query_list) == 1:
            _qry = self.query_list[0].strip().replace(" ", "+")
            self.url = [f"https://t.me/s/{self.channel_name}?q={_qry}"]
        elif len(self.query_list) > 1:
            _urls = []
            for n in range(len(self.query_list)):
                _qry = self.query_list[n].strip().replace(" ", "+")
                _urls.append(f"https://t.me/s/{self.channel_name}?q={_qry}")
            self.url = _urls


def validateSearch(search):
    if not (search.channel_name and search.query_list):
        return False
    else:
        return True
