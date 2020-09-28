from flask import current_app
import jwt
import time
from ...main import db
from ..models import UserModel, Address


def register_user(jsn):
    try:
        user = UserModel(jsn)
        user.put()
        return "registeration successful"
    except Exception as e:
        return str(e)

def jwt_encode(key, access, user_id):
    payload = {"role":role, "time":time.time()+360000, "user_id":user_id }
    jwt_code = jwt.encode(payload,key)
    return jwt_code.decode()

def login_user(jsn):
    try:
        if "email" in jsn.keys():
            user = UserModel.query.filter_by(email=jsn["email"]).first()
            if not user:
                return "No such user"
            else:
                if user.password == jsn["password"]:
                    key = current_app.config["SECRET_KEY"]
                    auth_code = jwt_encode(key, user.access, user.id)
                    return {"auth_code":auth_code, "message":"login successful"}
                else:
                    return "invalid credentials"

        else:
            user = UserModel.query.filter_by(phone=jsn["phone"]).first()
            if not user:
                return "no such user"
            else:
                if user.password == jsn["password"]:
                    key = current_app.config["SECRET_KEY"]
                    auth_code = jwt_encode(key, user.access, user.id)
                    return {"auth_code":auth_code, "message":"login successful"}
                else:
                    return "invalid credentials"
    except Exception as e:
        return str(e)

def delete_user(auth_code, jsn):
    auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
    if auth_decode["time"] < time:
        return "session expired, please login again"
    if auth_code["access"] = "admin":
        user = UserModel.query.filter_by(email=jsn["email"]).first()
        if not user:
            return "no such user"
        else:
            db.session.delete(user)
            db.session.commit()
            return "account removed"    
    else: # i.e. if access is user or owner, they can only remove themselves
        user = UserModel.query.filter_by(id=auth_decode["user_id"])
        db.session.delete(user)
        db.session.commit()
        return "account removed"

def address_edit(auth_code, jsn):
    auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
    if auth_decode["time"] < time.time():
        return "session expired, please login again"
    address = Address.query.filter_by(id=jsn["address_id"], user_id=auth_decode["user_id"]).first()
    if not address:
        return "invalid address id"

    if "name" in jsn.keys():
        address.country = jsn["name"]
    if "phone" in jsn.keys():
        address.phone = jsn["phone"]        
    if "country" in jsn.keys():
        address.country = jsn["country"]
    if "state" in jsn.keys():
        address.state = jsn["state"]    
    if "district" in jsn.keys():
        address.district = jsn["district"]
    if "city" in jsn.keys():
        address.city = jsn["city"]
    if "locality" in jsn.keys():
        address.locality = jsn["locality"]
    if "pincode" in jsn.keys():
        address.pincode = jsn["pincode"]                

    db.session.commit()
    return "adress modified"    

def address_edit(auth_code, jsn):
    auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
    if auth_decode["time"] < time.time():
        return "session expired, please login again"
    address = Address(auth_decode["user_id"], jsn)
    address.put()
    return "address added"

def address_list(auth_code):
    auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
    if auth_decode["time"] < time.time():
        return "session expired, please login again"
    addresses = Address.query.filter_by(user_id=auth_decode["user_id"]).all()
    if not addresses:
        return "no address found"
    res = []
    for each in addresses:
        row = {}
        row["city"] = each.city
        row["state"] = each.state
        row["locality"] = each.locality
        row["name"] = each.name
        row["phone"] = each.phone
        row["address_id"] = each.id
        res.append(row)
    return res    