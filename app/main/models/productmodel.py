from ...main import db
from .categorymodel import CategoryModel

class ProductModel(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, jsn):
        self.code = jsn["prod_code"]
        self.name = jsn["name"]
        self.price = jsn["price"]
        self.owner_id = jsn["owner_id"]

    def put(self):
        db.session.add(self)
        db.session.commit()

class ProductMetaModel(db.Model):
    __tablename__ = "productsMeta"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey("products.id", ondelete="CASCADE"))
    img_url = db.Column(db.String(500))
    description = db.Column(db.String(500))
    stock = db.Column(db.Integer)

    def __init__(self, jsn):
        self.product_id = jsn["product_id"]
        self.img_url = jsn["img_url"]
        self.description = jsn["description"]
        self.stock = jsn["stock"]

    def put(self):
        db.session.add(self)
        db.session.commit()

class ProductCategories(db.Model):
    __tablename__ = "product_categories"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"))
    db.UniqueConstraint("product_id","category_id")
