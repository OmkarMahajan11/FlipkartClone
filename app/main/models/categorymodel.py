from ...main import db

class CategoryModel(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def put(self):
        db.session.add(self)
        db.session.commit()

class Tree(db.Model):
    __tablename__ = "tree"
    descendant = db.Column(db.Integer,db.ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
    ancestor = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
    length = db.Column(db.Integer,nullable=False)

    def __init__(self, ancestor, descendant, length):
        self.ancestor = ancestor
        self.descendant = descendant
        self.length = length 

    def put(self):
        db.session.add(self)
        db.session.commit()