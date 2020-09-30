from flask import Blueprint
from flask import request
from ..services.userservice import register_user, login_user, delete_user, address_add, address_edit, address_list

user = Blueprint("user", __name__)

@user.route("/register", methods=["POST"])
def register():
    '''
    register user
    '''
    res = register_user(request.json)
    return {"result":res}

@user.route("/login", methods=["GET"])
def login():
    '''
    login user
    '''
    res = login_user(request.json)
    return {"result":res}

@user.route("/delete", methods=["DELETE"])
def delete():
    '''
    delete user
    '''
    auth_code = request.headers["auth_code"]
    res = delete_user(auth_code, request.json)
    return {"result":res}

@user.route("/address/add", methods=["POST"])
def add_address():
    '''
    add user address
    '''
    auth_code = request.headers["auth_code"]
    jsn = request.json
    res = address_add(auth_code, jsn)
    return {"result":res}

@user.route("/address/edit", methods=["POST"])
def edit_address():
    '''
    edit existing user address
    '''
    auth_code = request.headers["auth_code"]
    jsn = request.json
    res = address_edit(auth_code, jsn)
    return {"result":res}

@user.route("/address/list", methods=["GET"])
def list_address():
    auth_code = request.headers["auth_code"]
    res = address_list(auth_code)
    return {"result":res}