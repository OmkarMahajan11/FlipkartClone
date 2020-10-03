from flask import current_app
import jwt
import time
from ...main import db
from ..models import CommentModel, ProductModel

def comment_add(auth_code, jsn):
    try:
        auth_decode = jwt.decode(auth_code, current_app.config["SECRET_KEY"])
        if auth_decode['time'] <= time.time():
            return "time expired login again"
        user_id = auth_code['user_id']
        prod_id = jsn['product_id']
        item = ProductModel.query.filter_by(id=prod_id).first()
        if item == None:
            return "product not found"
        comment = CommentModel()
        comment.prod_id = prod_id
        comment.user_id = user_id
        comment.comment = jsn['comment']
        db.session.add(comment)
        db.session.commit()
        return "Comment added"    
    except Exception as e:
        return str(e)

def comment_show(product_id):
    rows =  CommentModel.query.filter_by(product_id=product_id).all()
    if not rows:
        return "no comments on this product"
    ls = []
    for each in rows:
        row = {}
        row['comment_id'] = each.id 
        row["comment"] = each.comment
        row["user_id"] = each.user_id
        row['upvotes'] = each.upvotes
        row['downvotes'] = each.downvotes
        ls.append(row)
    return ls    

def upvote(auth_head, jsn):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    comment_id = jsn['comment_id']
    comment = CommentModel.query.filter_by(id=comment_id).first()
    if comment == None:
        return "comment removed"
    if comment.upvotes == None:
        comment.upvotes = 1
    else:
        comment.upvotes = comment.upvotes+1
    db.session.commit()
    return "upvoted"

def downvote(auth_head, jsn):
    auth_code = jwt.decode(auth_head, current_app.config["SECRET_KEY"])
    if auth_code['time'] <= time.time():
        return "time expired login again"
    comment_id = jsn['comment_id']
    comment = CommentModel.query.filter_by(id=comment_id).first()
    if comment == None:
        return "comment removed"
    if comment.downvotes == None:
        comment.downvotes = 1
    else:
        comment.downvotes = comment.downvotes+1
    db.session.commit()
    return "downvoted"
