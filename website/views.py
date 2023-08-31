from flask import redirect, request, render_template, Blueprint
import os, signal, json
from .modules import add_channel, delete_channel, update_searches, load_searches

SEARCHESFILE = f"{os.getcwd()}/SearchesList.json"

views = Blueprint("views", __name__, template_folder="./templates")
searches = load_searches(SEARCHESFILE)


@views.route("/", methods=["GET"])
def home():
    return redirect(location="/index.html", code=301)


@views.route("/index.html", methods=["GET"])
def index():
    return render_template("index.html")


@views.route("/update.html", methods=["GET", "POST", "PUT", "DELETE"])
def updatepage():
    return render_template("update.html")


@views.route("/v1/queries/", methods=["GET"])
def get_queries():
    if request.method == "GET":
        try:
            searches = load_searches(SEARCHESFILE)
            if searches.fromkeys("status") != "error":
                return {"status": "OK", "saved_searches": searches}, 200
            elif searches.fromkeys("status") == "error":
                return searches, 400
        except Exception as e:
            print(f"Error in GET method:\n {e}")
            return {"Error from backend: ", e}, 500


@views.route("/v1/queries/<cname>", methods=["GET"])
def get_query(cname):
    if request.method == "GET":
        try:
            searches = load_searches(SEARCHESFILE)
            if str(cname).strip() in searches:
                return {"status": "OK", "saved_searches": searches[cname]}, 200
            else:
                return {
                    "status": "error",
                    "search": cname,
                    "error": "Channel doesn't exists in saved searches",
                }, 400
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
                    if str(q).strip() not in existing_queries:
                        existing_queries.append(q)
                update_searches(
                    query_list=existing_queries,
                    channel_name=cname,
                    searchfile=SEARCHESFILE,
                )
                return {
                    "status": "OK",
                    "updated search": cname,
                    "queries": existing_queries,
                }, 200
        except Exception as e:
            print(f"Error in PUT method:\n {e}")
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
                try:
                    queries: list = request_data.get("queries")
                    update_searches(queries, cname)
                    return {
                        "status": "OK",
                        "new search": f"{cname}",
                        "queries": queries,
                    }, 200
                except:
                    if request_data.get("queries") is None:
                        add_channel(channel_name=cname, searchfile=SEARCHESFILE)
                        print(f"{cname} added")
                        return {
                            "status": "OK",
                            "added channel": f"{cname}",
                        }, 200
        except Exception as e:
            print(f"Error in POST method:\n {e}")
            return {"Error from backend: ", e}, 500


@views.route("/v1/queries/<cname>", methods=["DELETE"])
def delete_query(cname):
    if request.method == "DELETE":
        try:
            request_data = request.json
            searches = load_searches(SEARCHESFILE)
            channels = searches.keys()
            if cname in channels and cname == request_data.get("channel_name"):
                try:
                    queries = request_data.get("queries")
                    existing_queries: list = searches.get(cname)
                    for q in queries:
                        if q in existing_queries:
                            existing_queries.remove(q)
                        elif q not in existing_queries:
                            pass
                    update_searches(
                        query_list=existing_queries,
                        channel_name=cname,
                        searchfile=SEARCHESFILE,
                    )
                    return {
                        "status": "OK",
                        "deleted search": f"{cname}",
                        "queries": queries,
                    }, 200
                except:
                    if request_data.get("queries") is None:
                        delete_channel(channel_name=cname, searchfile=SEARCHESFILE)
                        print(f"{cname} deleted")
                        return {
                            "status": "OK",
                            "deleted channel": f"{cname}",
                        }, 200
                    elif cname != request_data.get("channel_name"):
                        return {
                            "status": "error",
                            "search": cname,
                            "error": "Channel doesn't exists in saved searches",
                        }, 400

        except Exception as e:
            print(f"Error in DELETE method:\n {e}")
            return {"Error from backend: ", e}, 500


@views.route("/stop_server")
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return "Server stopped"
