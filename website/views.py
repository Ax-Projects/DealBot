from flask import Blueprint

views = Blueprint(__name__, "views")


@views.route("/", methods=["GET"])
def home():
    return "<h1>server is online</h1>", 200
