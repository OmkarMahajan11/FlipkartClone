from ..models.wishlistmodel import WishList
from ..models.productmodel import ProductModel, ProductMetaModel
from ...main import db
from flask import current_app
import time
import jwt

def wishlist_show(auth_code):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "session expired login again"
        user_id = auth_decode["user_id"]
        prod_ids = WishList.query.filter_by(user_id=user_id).all()
        if not prod_ids:
            return "wishlist is empty"
        res = []    
        for each in prod_ids:
            row = {}
            product = ProductModel.query.filter_by(id=each.id).first()
            meta = ProductMetaModel.query.filter_by(product_id=each.id).first()
            row["product_id"] = each.id
            row["product_name"] = product.name
            row["image"] = meta.img_url
            res.append(row)
        return res 
    except Exception as e:
        return str(e)       

def wishlist_remove(auth_code, product_id):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "session expired login again"
        user_id = auth_decode["user_id"]
        wl = WishList.query.filter_by(user_id=user_id, product_id=product_id)
        db.session.delete(wl)
        db.session.commit()
        return "product removed"
    except Exception as e:
        return str(e)    