from flask import redirect, request, render_template, Blueprint
import os, signal, json
from .modules import update_searches, load_searches

SEARCHESFILE = f"{os.getcwd()}/SearchesList.json"

views = Blueprint("views", __name__, template_folder="./templates")
searches = load_searches(SEARCHESFILE)


@views.route("/", methods=["GET"])
def home():
    return redirect(location="/index.html", code=301)


@views.route("/index.html", methods=["GET"])
def index():
    act = request.form
    print(act)
    return render_template("index.html", searches=searches, cnames=searches.keys())


@views.route("/update.html", methods=["GET", "POST", "PUT", "DELETE"])
def updatepage():
    return render_template("update.html", searches=searches, cnames=searches.keys())


@views.route("/v1/queries/", methods=["GET"])
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


@views.route("/v1/queries/<cname>", methods=["GET"])
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


@views.route("/v1/queries/<cname>", methods=["PUT"])
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


@views.route("/v1/queries/", methods=["POST"])
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


@views.route("/v1/queries/<cname>", methods=["DELETE"])
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


@views.route("/stop_server")
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return "Server stopped"
