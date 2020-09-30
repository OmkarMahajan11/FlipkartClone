from ...main import db
from .usermodel import UserModel
from .productmodel import ProductModel

class WishList(db.Model):
    __tablename__ ="wishlist"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))

    def __init__(self, user_id, product_id):
        self.product_id = product_id
        self.user_id = user_id

    def put(self):
        db.session.add(self)
        db.session.commit() 