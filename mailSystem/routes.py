from flask import render_template, request, session, flash
from mailSystem.models import *
from mailSystem.sendmail import pushmail
from mailSystem import app

@app.route('/')
def mailsys():
    headings = ("Name", "Email", "Contact", "Option")
    cus = db.session.query(Customer)
    return render_template('sendmail.html', headings=headings, customers=cus)


@app.route('/custom_mail', methods=['POST'])
def custom_mail():
    if request.method == 'POST':
        mail_list = request.form.getlist('culist')
        subject = request.form['subject']
        content = request.form['content']
        print(mail_list, subject, content)
        pushmail.pushmails(mail_list, subject, content)
        return "worked"



@app.route('/change_status', methods=['GET'])
def change_status():
    if request.method == 'GET':
        # value = request.form['status_val']
        # if value == "change_stat":
        header = ('order id', 'customer id', 'ordered date', 'shipped date', 'delivered date')
        order = db.session.query(Order)
        return render_template('push_order_status.html', headers=header, orders=order)



# change name and make so that you have to pass at least 1 value
@app.route('/push_status', methods=['POST'])
def push_status():
    if request.method == 'POST':
        if request.form.get('push_to_ship') == "move orders to Shipped":
            orders_li = request.form.getlist('change_stat')
            # if orders_li:
            for i in orders_li:

                if db.session.query(Order.shipped_date).filter(Order.id == i).scalar() is None:
                    db.session.query(Order).filter_by(id=i).update(
                        dict(shipped_date=datetime.now().strftime("%Y-%m-%d, %H:%M")))
                    cu = db.session.query(Order.customer_id).filter(Order.id == i).scalar()
                    email_id = db.session.query(Customer.email).filter(Customer.id == cu).scalar()
                    pushmail.shipped(email_id)

                    return render_template('push_order_status.html')
                else:
                    flash("Please select orders that arent already Shipped.")
                    return render_template('push_order_status.html')
            # else:
            #     return "weelpppp"

        elif request.form.get('push_to_deliv') == "move orders to Delivered":
            orders_li = request.form.getlist('change_stat')
            for i in orders_li:
                if db.session.query(Order.shipped_date).filter(Order.id == i).scalar() is not None and db.session.query(Order.delivered_date).filter(Order.id == i).scalar() is None:
                    db.session.query(Order).filter_by(id=i).update(
                        dict(delivered_date=datetime.now().strftime("%Y-%m-%d, %H:%M")))
                    cu = db.session.query(Order.customer_id).filter(Order.id == i).scalar()
                    email_id = db.session.query(Customer.email).filter(Customer.id == cu).scalar()
                    pushmail.delivered(email_id)
                    return render_template('push_order_status.html')
                else:
                    flash("Please select orders that are shipped and not yet delivered.")
                    return render_template('push_order_status.html')



# Registeration page
@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


# submitting registration page and redirect to make order
@app.route('/submit', methods=['POST'])
def submit():

    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']

        customer = Customer(fname, lname, dob, email, phone)
        db.session.add(customer)
        db.session.commit()
        pushmail.welcome(email)

        current_id = db.session.query(Customer.id).filter(Customer.email == email).scalar()
        session['value'] = current_id

        return render_template('makeOrder.html', fname=fname, id=current_id)


@app.route('/submitOrder', methods=['POST'])
def submitOrder():
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
        db.session.close()
        # session.clear()
        return "success"


@app.route('/test', methods=['GET'])
def test():
    current_id = str(session.get("value"))
    return current_id
