from flask import Blueprint
from flask import request
from ..services.cartservice import cart_display, cart_inc, cart_dec, cart_delete, cart_checkout

cart = Blueprint("cart", __name__)

@cart.route("/display", methods=["GET"])
def display():
    auth_code = request.headers["auth_code"]
    res = cart_display(auth_code)
    return {"result":res}

@cart.route("/inc/<product_id>", methods=["POST"])
def inc(product_id):
    auth_code = request.headers["auth_code"]
    res = cart_inc(auth_code, product_id)
    return {"result":res}

@cart.route("/dec/<product_id>", methods=["POST"])
def dec(product_id):
    auth_code = request.headers["auth_code"]
    res = cart_dec(auth_code, product_id)
    return {"result":res}

@cart.route("/delete/<product_id>", methods=["POST"])
def delete(product_id):
    auth_code = request.headers["auth_code"]
    res = cart_delete(auth_code, product_id)
    return {"result":res}

@cart.route("/checkout", methods=["POST"])    
def checkout():
    auth_code = request.headers["auth_code"]
    res = cart_checkout(auth_code)
    return {"result":res}