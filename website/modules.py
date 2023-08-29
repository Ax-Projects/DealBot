import json

# SEARCHESFILE = "../SearchesList.json"


def load_searches(file_path) -> dict:
    try:
        with open(file_path, encoding="utf-16") as file:
            json_data: dict = json.load(file)
        return json_data
    except FileNotFoundError:
        return {
            "status": "error",
            "reason": "search list file is un-accessible",
        }


def update_searches(query_list, channel_name: str) -> None:
    searches = load_searches(SEARCHESFILE)
    searches[channel_name] = query_list
    with open(SEARCHESFILE, "w", encoding="utf-16") as file:
        json.dump(searches, file)
