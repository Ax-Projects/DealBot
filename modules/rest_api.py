from flask import Flask, request, render_template
import os
import signal
import json

SEARCHESFILE = f"{os.getcwd()}/SearchesList.json"
HOMEPAGE = f"{os.getcwd()}/website/"


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
    return render_template("index.html", searches=searches, cnames=searches.keys())


@app.route("/v1/queries/", methods=["GET"])
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


@app.route("/v1/queries/<cname>", methods=["GET"])
def get_query(cname):
    if request.method == "GET":
        try:
            searches = load_searches(SEARCHESFILE)
            if cname in searches:
                return {"status": "OK", "saved_searches": searches[cname]}, 200
            else:
                return {
                    "status": "error",
                    "search": cname,
                    "error": "Channel doesn't exists in saved searches",
                }, 500
        except Exception as e:
            print(f"Error in GET method:\n {e}")
            return {"Error from backend: ", e}, 500


@app.route("/v1/queries/<cname>", methods=["PUT"])
def update_query(cname):
    if request.method == "PUT":
        try:
            request_data = request.json
            searches = load_searches(SEARCHESFILE)
            if cname in searches and cname == request_data.get("channel_name"):
                queries = request_data.get("queries")
                existing_queries = searches[cname]
                for q in queries:
                    if q not in existing_queries:
                        existing_queries.append(q)
                update_searches(existing_queries, cname)
                return {
                    "status": "OK",
                    "updated search": cname,
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
            searches = load_searches(SEARCHESFILE)
            channels = searches.keys()
            cname = request_data.get("channel_name")
            if cname not in channels:
                queries: list = request_data.get("queries")
                update_searches(queries, cname)
                return {
                    "status": "OK",
                    "new search": f"{cname}",
                    "queries": queries,
                }, 200
        except Exception as e:
            print(f"Error in GET method:\n {e}")
            return {"Error from backend: ", e}, 500


@app.route("/v1/queries/<cname>", methods=["DELETE"])
def delete_query(cname):
    if request.method == "DELETE":
        try:
            request_data = request.json
            searches = load_searches(SEARCHESFILE)
            channels = searches.keys()
            if cname in channels and cname == request_data.get("channel_name"):
                queries = request_data.get("queries")
                existing_queries: list = searches.get(cname)
                for q in queries:
                    if q in existing_queries:
                        existing_queries.remove(q)
                    elif q not in existing_queries:
                        pass
                update_searches(existing_queries, cname)
                return {
                    "status": "OK",
                    "deleted search": f"{cname}",
                    "queries": queries,
                }, 200
        except Exception as e:
            print(f"Error in GET method:\n {e}")
            return {"Error from backend: ", e}, 500


@app.route("/stop_server")
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return "Server stopped"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
