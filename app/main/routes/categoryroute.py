from flask import Blueprint
from flask import request
from ..services.categoryservice import category_add, category_show, category_sub

category = Blueprint("category", __name__)

@category.route("/add", methods=["POST"])
def add_cat():
    auth_code = request.headers["auth_code"]
    res = category_add(auth_code, request.json)
    return {"result":res}

@category.route("/show")
def show():
    res = category_show()
    return {"result":res}

@category.route("/show/<category_name>")
def show_cat(category_name):
    res = category_sub(category_name)
    return {"result":res}