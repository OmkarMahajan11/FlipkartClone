from ...main import db
from .usermodel import User
from .productmodel import ProductModel

class WishList(db.Model):
    __tablename__ ="wishlist"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
