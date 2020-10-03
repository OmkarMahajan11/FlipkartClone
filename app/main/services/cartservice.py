from flask import current_app
import time
import jwt
from ..models.cartmodel import CartModel
from ..models.productmodel import ProductModel, ProductMetaModel
from ...main import db


def cart_display(auth_code):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "session expired login again"
        user_id = auth_decode["user_id"]
        cartRows = CartModel.query.filter_by(user_id=user_id).all()
        if not cartRows:
            return "cart is empty"
        res = []
        net_price = 0
        for each in cartRows:
            product = ProductModel.query.filter_by(product_id=each.product_id).first()
            meta = ProductMetaModel.query.filter_by(product_id=each.product_id).first()
            row = {}
            row["name"] = product.name
            row["image"] = meta.img_url
            row["price"] = product.price
            row["quantity"] = each.quantity
            net_price += each.quantity * product.price
            res.append(row)
        return {"user_id":user_id, "total":net_price, "products":res}
    except Exception as e:
        return str(e)    


def cart_inc(product_id):
    try:
        cartRow = CartModel.query.filter_by(product_id=product_id).first()
        cartRow.quantity += 1
        db.session.commit()
    except Exception as e:
        str(e)


def cart_dec(product_id):
    try:
        cartRow = CartModel.query.filter_by(product_id=product_id).first()
        cartRow.quantity -= 1
        db.session.commit()
    except Exception as e:
        str(e)


def cart_delete(product_id):
    try:
        cartRow = CartModel.query.filter_by(product_id=product_id).first() 
        db.session.delete(cartRow)
        db.session.commit()
    except Exception as e:
        return str(e)    

def cart_checkout():
    return

def cart_add(auth_code, product):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "session expired login again"
        user_id = auth_decode["user_id"]
        product_id = ProductModel.query.filter_by(name=product).first()
        ct = CartModel.query.filter_by(user_id=user_id, product_id=product_id)
        if ct: #i.e. product already in cart then, increase quantity
            ct.quantity += 1
            db.session.commit()
        else:
            addCart = CartModel(user_id, product_id, 1)
            addCart.put()    
    except Exception as e:
        return str(e)
