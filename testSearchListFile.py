import json, os
import searchQueries

file = f"{os.getcwd()}/SearchesList.json"
with open(file) as f:
    searchList: dict = json.load(f)

# searches = []
# for i in range(len(searchList)):
#     search = f"s{i}"
#     globals()[search] = None
#     searches.append(search)

# for i, k in zip(searches, searchList):
#     x = searchQueries.Search(k, searchList[k])
#     globals()[i] = x

# print(s0.url)

for t in searchList.keys():
    print(t)
    print(searchList[t])
    x = searchQueries.Search(t, searchList[t])
    print(type(x))
