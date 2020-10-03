from ...main import db 

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    phone = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    access = db.Column(db.String(10), nullable=False)

    def __init__(self, jsn):
        self.name = jsn["name"]
        self.email = jsn["email"]
        self.phone = jsn["phone"]
        self.password = jsn["password"]
        self.access = jsn["access"]

    def put(self):
        db.session.add(self)
        db.session.commit()    

class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"))
    name = db.Column(db.String(70), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    country = db.Column(db.String(70))
    state = db.Column(db.String(70))
    district = db.Column(db.String(70))
    city = db.Column(db.String(70))
    locality = db.Column(db.String(70))
    pincode = db.Column(db.String(10),nullable=False)    

    def __init__(self, user_id, jsn):
        self.user_id = user_id
        self.name = jsn['name']
        self.phone = jsn['mobile_no']
        self.country = jsn['country']
        self.state = jsn['state']
        self.district = jsn['district']
        self.city = jsn['city']
        self.locality = jsn['locality']
        self.pincode = jsn['pincode']

    def put(self):
        db.session.add(self)
        db.session.commit()    

class PaymentInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "cascade"))
    name = db.Column(db.String(100), nullable=False)
    pay_num = db.Column(db.Integer)
    pay_type = db.Column(db.String(10))

    def __init__(self, user_id, jsn):
        self.user_id = user_id
        self.name = jsn["name"]
        self.pay_type = jsn["payment_type"]
        self.pay_num = jsn["payment_number"]

    def put(self):
        db.session.add(self)
        db.session.commit()    