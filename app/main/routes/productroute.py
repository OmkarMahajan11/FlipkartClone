from flask import Blueprint
from flask import request
from ..services.productservice import product_add, prod_search, product_cat, product_edit, product_meta_add, product_show, wishlist_add, cart_add

product = Blueprint("product", __name__)

@product.route("/add", methods=["POST"])
def add_product():
    auth_code = request.headers["auth_code"]
    res = product_add(auth_code, request.json)
    return {"result":res}

@product.route("/edit", methods=["POST"])
def edit_product():
    auth_code = request.headers["auth_code"]
    res = product_edit(auth_code, request.json)
    return {"result":res}

@product.route("/show", methods=["GET"])
def show():
    page = request.args.get("page", default=1, type=int)
    itemsPerPage = 10
    res = product_show(page, itemsPerPage)
    return {"result":res}

@product.route("/addmeta", methods=["POST"])
def add_meta():
    auth_code = request.headers["auth_code"]
    res = product_meta_add(auth_code, request.json)
    return {"result":res}

@product.route("/editmeta", methods=["POST"])
def edit_meta():
    auth_code = request.headers["auth_code"]
    res = product_meta_add(auth_code, request.json)
    return {"result":res}

@product.route("/assign/category", methods=["POST"])
def assign_category():
    auth_code = request.headers["auth_code"]
    res = product_cat(auth_code, request.json)
    return {"result":res}

@product.route("/search/<category>", methods= ['GET'])
def search(category):
    res = prod_search(category)
    return {"result": res}

@product.route("/add/wishlist/<product>", methods=["POST"])
def addwish(product):
    auth_code = request.headers["auth_code"]
    res = wishlist_add(auth_code, product)
    return {"result":res}

@product.route("/add/cart/<product>", methods=["POST"])
def addToCart(product):
    auth_code = request.headers["auth_code"]
    res = cart_add(auth_code, product)
    return {"result":res}