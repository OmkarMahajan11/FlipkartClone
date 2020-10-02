from flask_sqlalchemy import sqlalchemy
from flask import current_app
import time
import jwt
from ..models import UserModel
from ..models import ProductModel, ProductMetaModel, ProductCategories
from ..models import CategoryModel, Tree
from ..models import WishList
from ..models import CartModel
from ...main import db


def product_add(auth_code, jsn):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "time expired login again"
        if auth_decode['access'] != "owner":
            return "only owner allowed to add products"

        prod_code = jsn["prod_code"]
        row = ProductModel.query.filter_by(code=prod_code).first()
        if row:
            return "product already present"
        prod = ProductModel(jsn)
        prod.put()
        return "product added"
    except Exception as e:
        return str(e)    

def product_edit(auth_code, jsn):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "time expired login again"
        if auth_decode['access'] == "user":
            return "access denied, owner or admin access required"
        prod_id = jsn["prod_id"]
        product = ProductModel.query.filter_by(code=prod_id).first()
        if not product:
            return "no such product"
        if auth_code['access'] == "owner":    
            if product.owner_id != auth_decode["user_id"]:
                return "not the owner of the product"
        
        if 'prod_code' in jsn.keys():
            product.code = jsn['prod_code']
        if 'name' in jsn.keys():
            product.name = jsn['name']
        if 'price' in jsn.keys():
            product.price = jsn['price']
        db.session.commit()
        return "product edited"        
    except Exception as e:
        return str(e)

def product_show(page, itemsPerPage):
    products = ProductModel.query.all()
    ls = []
    for each in products:
        row = {}
        row["product_id"] = each.id
        row["name"] = each.name
        row["price"] = each.price
        meta = ProductMetaModel.query.filter_by(product_id=each.id).first()
        if not meta:
            row["image"] = None
            row["description"] = None
        else:
            row["image"] = meta.img_url
            row["description"] = meta.description    
        ls.append(row)
    return ls[(page-1)*itemsPerPage:page*itemsPerPage]

def product_meta_add(auth_code, jsn):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "time expired login again"
        if auth_decode['access'] == "user":
            return "access denied, owner or admin access required"
        owner = ProductModel.query.filter_by(id=jsn['prod_id']).first()
        if owner == None:
            return "product not found"
        if owner.owner_id != auth_decode['user_id']:
            return "unauthorized to access the product"
        meta = ProductMetaModel.query.filter_by(product_id=jsn['product_id']).first()
        if not meta:
            prodMeta = ProductMetaModel(jsn)
            prodMeta.put()
            return "meta info added"
        else:
            if "img_url" in jsn.keys():
                meta.img_url = jsn["img_url"]
            if "description" in jsn.keys():
                meta.description = jsn["description"]
            if "stock" in jsn.keys():
                meta.stock = jsn["stock"]    
            db.session.commit()
            return "meta info edited"
    except Exception as e:
        return str(e)        

def product_cat(auth_code, jsn):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "time expired login again"
        if auth_decode['access'] == "user":
            return "access denied, owner or admin access required"
        product_id = jsn["product_id"]
        category_id = jsn["category_id"]    
        product = ProductModel.query.filter_by(id=product_id).first()
        if not product:
            return "no such product"
        ancestors = Tree.query.filter_by(descendant=category_id).all()
        for each in ancestors:
            data = ProductCategories.query.filter_by(category_id=each.id, product_id=product_id)    
            if not data:
                pc = ProductCategories()
                pc.category_id = each.ancestor
                pc.product_id = product_id
                db.session.add(pc)
                db.session.commit()
        return "category assigned"    
    except Exception as e:
        return str(e)

def prod_search(category):
    try:
        query = "select p.name, p.price,p.id from products as p join product_categories as pc on pc.product_id = p.id join categories as c  on c.id = pc.category_id where c.name like '%{}%' ;".format(category)
        products = db.session.execute(query)
        ls = []
        for each in products:
            row= {}
            row['id'] = each.id
            row['name'] = each.name
            row['price'] = each.price
            meta = ProductMetaModel.query.filter_by(product_id=each.id).first()
            if meta != None:
                row["image"] = meta.img_url    
            else:
                row["image"] = None
            ls.append(row)
        if len(ls)==0:
            return "no products found"
        return ls
    except Exception as e:
        return str(e)

def wishlist_add(auth_code, product):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "session expired login again"
        user_id = auth_decode["user_id"]
        product_id = ProductModel.query.filter_by(name=product).first()
        if not product_id:
            return "no such product"
        wl = WishList.query.filter_by(user_id=user_id, product_id=product_id)
        if not wl:    
            addToWish = WishList(user_id, product_id)
            addToWish.put()
            return "product added to wishlist"
        return "already in the wishlist"        
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