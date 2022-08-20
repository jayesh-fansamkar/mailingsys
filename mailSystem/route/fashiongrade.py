from flask import Blueprint, render_template, request, session
from mailSystem.models import *
from mailSystem.sendmail import pushmail

shop = Blueprint("shop", __name__)


# Registration page
@shop.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


# submitting registration page and redirect to make order
@shop.route('/submit', methods=['POST'])
def submit():

    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']

        if db.session.query(Customer.email).filter_by(email=email).scalar() is None:
            customer = Customer(fname, lname, dob, email, phone)
            db.session.add(customer)
            db.session.commit()
            pushmail.welcome(email)

            current_id = db.session.query(Customer.id).filter(Customer.email == email).scalar()
            session['value'] = current_id

            return render_template('makeOrder.html', fname=fname, id=current_id)
        else:
            return render_template('inuse.html')


@shop.route('/submitOrder', methods=['POST'])
def submit_order():
    customer_id = session.get("value")
    if request.method == 'POST':
        val = request.form['choice']
        if val == 'pack1':
            product = db.session.query(Product).filter_by(id=1)
        elif val == 'pack2':
            product = db.session.query(Product).filter_by(id=2)
        order = Order(customer_id=customer_id, products=product)

        db.session.add(order)
        db.session.commit()
        email_id = db.session.query(Customer.email).filter(Customer.id == customer_id).scalar()
        pushmail.ordered(email_id)
        session.clear()
        return render_template('completed.html')
