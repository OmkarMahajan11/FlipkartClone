from flask import Blueprint
from flask import request
from ..services.commentservice import comment_show, upvote, downvote


comment = Blueprint("comment", __name__)


@comment.route("/show", methods=["GET"])
def show_comment():
    res = comment_show(request.json["product_id"])
    return {"result":res}

@comment.route("/upvote", methods=['POST'])
def upvoted():
    auth_code = request.headers['auth_code']
    jsn = request.json
    res = upvote(auth_code, jsn)
    return {"result": res}

@comment.route("/downvote", methods=['POST'])
def downvoted():
    auth_code = request.headers['auth_code']
    jsn = request.json
    res = downvote(auth_code, jsn)
    return {"result": res}