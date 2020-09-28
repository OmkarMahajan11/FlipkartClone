from ...main import db

class CartModel(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    quantity = db.Column(db.Integer)
    db.CheckConstraint(quantity>0)

    def __init__(self, jsn):
        self.product_id = jsn["product_id"]
        self.user_id = jsn["user_id"]
        self.quantity = jsn["quantity"]

    def put(self):
        db.session.add(self)
        db.session.commit()    