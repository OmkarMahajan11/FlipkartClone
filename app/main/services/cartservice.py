from flask import current_app
import time
import jwt
from ..models.cartmodel import CartModel
from ..models.usermodel import Address, UserModel
from ..models.productmodel import ProductModel, ProductMetaModel
from ..models.ordermodel import OrderDetails, Order, Payment
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


def cart_inc(auth_code, product_id):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "session expired login again"
        user_id = auth_decode["user_id"]
        cartRow = CartModel.query.filter_by(user_id=user_id, product_id=product_id).first()
        cartRow.quantity += 1
        db.session.commit()
    except Exception as e:
        str(e)


def cart_dec(auth_code, product_id):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "session expired login again"
        user_id = auth_decode["user_id"]
        cartRow = CartModel.query.filter_by(user_id=user_id, product_id=product_id).first()
        cartRow.quantity -= 1
        db.session.commit()
    except Exception as e:
        str(e)


def cart_delete(auth_code, product_id):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "session expired login again"
        user_id = auth_decode["user_id"]
        cartRow = CartModel.query.filter_by(user_id=user_id, product_id=product_id).first() 
        db.session.delete(cartRow)
        db.session.commit()
    except Exception as e:
        return str(e)    

def cart_checkout(auth_code, jsn):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "time expired login again"
        address = Address.query.filter_by(user_id=auth_code['user_id']).first()    
        if not address:
            return "no adress found please add"
        query = """SELECT c.quantity as quantity, mp.stock as stock, p.id as product_id, p.name as name, p.price as price FROM cart as c JOIN products as p ON p.id=c.product_id JOIN productsMeta as mp ON mp.product_id=p.id WHERE c.user_id={};""".format(auth_decode["user_id"]) 
        rows = db.session.execute(query)

        ls = []
        for each in rows:
            ls.append(each)
        if len(ls) == 0:
            return "cart empty"
        for each in ls:
            if each.quantity > each.stock:
                return "{} not available".format(each.name)

        net_price = 0
        for each in ls:
            net_price = net_price + (each.quantity*each.price)

        pay = Payment()
        pay.payment_amount = net_price
        pay.payment_method = jsn["payment_mode"]
        pay.user_id = auth_decode["user_id"]    
        db.session.add(pay)
        db.session.commit()

        order = Order()
        order.order_value = net_price
        order.user_id = auth_decode["user_id"]
        order.payment_id = pay.id
        order.order_status = "Initiated"
        order.address_id = jsn["address_id"]
        db.session.add(order)
        db.session.commit()

        for each in ls:
            order_det = OrderDetails()
            order_det.order_id = order.id
            order_det.product_id = each.product_id
            order_det.quantity = each.quantity
            order_det.cost = each.quantity * each.price
            db.session.add(order_det)
            db.session.commit()

        cartRows = CartModel.query.filter_by(user_id=auth_decode["user_id"]).all()
        for each in cartRows:
            db.session.delete(each)
            db.session.commit()

        return "order placed, your order id = {}".format(order.id)        
    except Exception as e:
        return str(e)

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
