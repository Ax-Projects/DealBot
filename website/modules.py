import json
import os

# SEARCHESFILE = "../SearchesList.json"


def load_searches(file_path) -> dict:
    try:
        with open(file_path, encoding="utf-16") as file:
            json_data: dict = json.load(file)
        return json_data
    except FileNotFoundError:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-16") as file:
                json.dump({}, file)
        return {
            "status": "error",
            "reason": "search list file is un-accessible.",
        }


def add_channel(channel_name: str, searchfile: str) -> None:
    searches: dict = load_searches(searchfile)
    searches[channel_name] = []
    with open(searchfile, "w", encoding="utf-16") as file:
        json.dump(searches, file)


def update_searches(query_list, channel_name: str, searchfile: str) -> None:
    searches = load_searches(searchfile)
    searches[channel_name] = query_list
    with open(searchfile, "w", encoding="utf-16") as file:
        json.dump(searches, file)


def delete_channel(channel_name: str, searchfile: str) -> None:
    searches = load_searches(searchfile)
    print(searches)
    searches.pop(channel_name)
    print(searches)
    with open(searchfile, "w", encoding="utf-16") as file:
        json.dump(searches, file)
