from flask_sqlalchemy import sqlalchemy
from flask import current_app
import time
import jwt
from ..models.categorymodel import CategoryModel , Tree 
from ...main import db

def category_add(auth_code, jsn):
    auth_code = jwt.decode(auth_code,current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    if auth_code['role']!="admin":
        return "permission denied admin access required"
    
    category = CategoryModel.query.filter_by(name=jsn["name"]).first()
    if category:
        return "category already present"

    if jsn["ancestor"] == jsn["name"]:
        newCat = CategoryModel(jsn["name"])
        newCat.put()
        cat_id = CategoryModel.query.filter_by(name=jsn["name"]).first().id
        catTree = Tree(cat_id, cat_id, 0) 
        catTree.put()
        return "category added"
    else:
        ancestor = CategoryModel.query.filter_by(name=jsn["ancestor"]).first()
        if not ancestor:
            return "ancestor category invalid"
        newCat = CategoryModel(jsn["name"])
        newCat.put()
        cat_id = CategoryModel.query.filter_by(name=jsn["name"]).first().id
        catTree = Tree.query.filter_by(descendant=ancestor.id).all()
        for each in catTree:
            newToTree = Tree(each.id, cat_id, each.length+1)
            newToTree.put()
        newToTree = Tree(cat_id, cat_id, 0)
        newToTree.put()
        return "category added"

def category_show():
    query = """SELECT * FROM categories as cat join (descendant, count(*) as c FROM tree GROUP BY 1) as t on cat.id = t.descendant where t.c=1"""     
    main_categories = db.session.execute(query)
    res = []
    for each in main_categories:
        res.append(each.name)
    return res 

def category_sub(cat_name):
    check = CategoryModel.query.filter_by(name=cat_name).first()
    if not check:
        return "category does not exist"
    query = """SELECT * FROM categories as cat JOIN tree as t ON cat.id=t.descendant WHERE t.ancestor={} and t.length=1""".format(check.id)    
    subCategories = db.session.execute(query)
    res = []
    for each in subCategories:
        res.append(each.name)
    return res    