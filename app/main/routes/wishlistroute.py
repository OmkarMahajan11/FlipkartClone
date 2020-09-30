from flask import Blueprint
from flask import request
from ..services.wishlistservice import wishlist_show, wishlist_remove 

wishlist = Blueprint("wishlist", __name__)

@wishlist.route("/show", methods=["GET"])
def show():
    auth_code = request.headers["auth_code"]
    res = wishlist_show(auth_code)
    return {"result":res}

@wishlist.route("/remove/<product_id>")
def remove(product_id):
    auth_code = request.headers["auth_code"]
    res = wishlist_remove(auth_code, product_id)
    return {"result":res}
