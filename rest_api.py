from flask import Flask, request, render_template
import os
import signal
import json

SEARCHESFILE = f"{os.getcwd()}/SearchesList.json"


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


searches = load_searches(SEARCHESFILE)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return "server is online", 200


@app.route("/v1/queries/", methods=["GET", "DELETE", "PUT"])
def get_queries():
    if request.method == "GET":
        try:
            searches = load_searches(SEARCHESFILE)
            if searches.fromkeys("status") != "error":
                return {"status": "OK", "saved_searches": searches}, 200
            elif searches.fromkeys("status") == "error":
                return searches, 500
        except Exception as e:
            print(f"Error in GET method:\n {e}")
            return {"Error from backend: ", e}, 500


@app.route("/v1/queries/<cname>", methods=["PUT"])
def update_query(cname):
    if request.method == "PUT":
        try:
            request_data = request.json
            # Checking if search channel already exists in the searches list
            searches = load_searches(SEARCHESFILE)
            channels = searches.keys()
            if cname in channels:
                # TODO: add logic to insert new search query terms in the search list
                queries: dict = request_data.get("queries")
                existing_queries: dict = searches.get(cname)
                for q in queries:
                    if q in existing_queries:
                        pass
                    elif q not in existing_queries:
                        existing_queries.append(q)
                update_searches(existing_queries, cname)
                return {
                    "status": "OK",
                    "updated search": f"{cname}",
                    "queries": existing_queries,
                }, 200
        except Exception as e:
            print(f"Error in GET method:\n {e}")
            return {"Error from backend: ", e}, 500


@app.route("/v1/queries/", methods=["POST"])
def new_query():
    if request.method == "POST":
        try:
            request_data = request.json
            # Checking if search channel already exists in the searches list
            searches = load_searches(SEARCHESFILE)
            channels = searches.keys()
            cname = request_data.get("channel_name")
            if cname not in channels:
                # TODO: add logic to insert new search query terms in the search list
                queries: dict = request_data.get("queries")
                update_searches(queries, cname)
                return {
                    "status": "OK",
                    "new search": f"{cname}",
                    "queries": queries,
                }, 200
        except Exception as e:
            print(f"Error in GET method:\n {e}")
            return {"Error from backend: ", e}, 500


# elif request.method == "POST":
#     try:
#         request_data = request.json
#         # Checking if search channel already exists in the searches list
#         channels = searches.keys()
#         if request_data.get("channel_name") in channels:
#             # TODO: add logic to insert new search query terms in the search list

#             return {"status": "OK", "new search": "Channel already exists"}, 500
#         # Checking if user_id exists in the DB
#         userData = db.get_user_data(user_id)
#         if userData != None:
#             return {"status": "error", "reason": "ID already exists"}, 500
#         else:
#             # Checking if the Json payload contains user_name
#             try:
#                 user_nm = request_data.get("user_name")
#             except:
#                 user_nm = None
#             if user_nm is not None:
#                 # Using DB method to create a new user
#                 status = db.create_user(user_id=user_id, user_name=user_nm)
#                 # Checking DB method result
#                 if status == True:
#                     return {"status": "OK", "user_added": user_nm}, 200
#                 else:
#                     return {f"error": status}, 400
#             elif user_nm == None:
#                 print(
#                     "user_name is not specified in the POST request's payload"
#                 )  # Print if JSON payload doesn't contain user_name
#     except Exception as e:
#         print(f"Error in  POST method:\n {e}")

# elif request.method == "PUT":
#     try:
#         request_data = request.json
#         # Checking if user_id exists in the DB
#         userData = db.get_user_data(user_id)
#         if userData == None:
#             return {"status": "error", "reason": "No such ID"}, 500
#         elif userData != None:
#             newUserName = request_data.get("user_name")
#             status = db.update_user(user_id=userData, user_name=newUserName)
#             if status == True:
#                 return {"status": "OK", "user_updated": userData}, 200
#             else:
#                 return {f"sql error": status}, 400
#         else:
#             return {"status": "error", "reason": status}, 400
#     except Exception as e:
#         print(f"Error in  PUT method:\n {e}")

# elif request.method == "DELETE":
#     # Error catching in DELETE request for user name by user_id
#     try:
#         userData = db.get_user_data(user_id)
#         if userData == None:
#             return {"status": "error", "reason": "no such id"}, 500
#         else:
#             status = db.delete_user(user_id)
#             if status == True:
#                 return {"status": "OK", "user_deleted": user_id}, 200
#             else:
#                 return {"sql error": status}, 400
#     except Exception as e:
#         print(f"Error in DELETE method:\n {e}")


@app.route("/stop_server")
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return "Server stopped"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
