from mailSystem import db
from datetime import datetime


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40), unique=False, nullable=False)
    lname = db.Column(db.String(40), unique=False, nullable=False)
    dob = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=False, nullable=True)

    orders = db.relationship('Order', backref='customer')

    def __init__(self, fname, lname, dob, email, phone):
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.email = email
        self.phone = phone


order_product = db.Table('order_product',
                         db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
                         db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
                         )


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now().strftime("%Y-%m-%d, %H:%M"))
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)

    products = db.relationship('Product', secondary=order_product)

    def __init__(self, customer_id, products):
        self.customer_id = customer_id
        self.products = list(products)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)


class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    last = db.Column(db.String(40), unique=False, nullable=False)

# db.create_all()
# package1 = Product(name="package1", price="500")
# package2 = Product(name="package2", price="1000")
# db.session.add(package1)
# db.session.add(package2)
# db.session.commit()
