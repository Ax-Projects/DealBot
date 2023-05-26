import json, os
import searchQueries

file = f"{os.getcwd()}/SearchesList.json"
with open(file) as f:
    searchList = json.load(f)

searches = []
for i in range(len(searchList)):
    search = f"s{i}"
    globals()[search] = None
    searches.append(search)

for i, k in zip(searches, searchList):
    x = searchQueries.Search(k, searchList[k])
    globals()[i] = x

print(s0.url)
