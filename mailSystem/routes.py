from flask import render_template, request, session, redirect, flash
from mailSystem.models import *
from mailSystem.sendmail import pushmail
from mailSystem import app


@app.route('/', methods=['GET'])
def mailsys():
    headings = ("Id", "Name", "Email", "Contact", "Option")
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
        return mailsys()


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
                else:
                    flash("Please select orders that arent already Shipped.")
                    return redirect('change_status')
            return redirect('change_status')
        elif request.form.get('push_to_deliv') == "move orders to Delivered":
            orders_li = request.form.getlist('change_stat')
            for i in orders_li:
                if db.session.query(Order.shipped_date).filter(Order.id == i).scalar() is not None and db.session.query(
                        Order.delivered_date).filter(Order.id == i).scalar() is None:
                    db.session.query(Order).filter_by(id=i).update(
                        dict(delivered_date=datetime.now().strftime("%Y-%m-%d, %H:%M")))
                    cu = db.session.query(Order.customer_id).filter(Order.id == i).scalar()
                    email_id = db.session.query(Customer.email).filter(Customer.id == cu).scalar()
                    pushmail.delivered(email_id)
                else:
                    flash("Please select orders that are shipped and not yet delivered.")
                    return redirect('change_status')
            return redirect('change_status')
        elif request.form.get('delete') == "delete order status":
            orders_li = request.form.getlist('change_stat')
            for i in orders_li:
                if db.session.query(Order.delivered_date).filter(Order.id == i).scalar() is not None:
                    db.session.query(Order).filter_by(id=i).update(dict(delivered_date=None))

                elif db.session.query(Order.shipped_date).filter(Order.id == i).scalar() is not None:
                    db.session.query(Order).filter_by(id=i).update(dict(shipped_date=None))

                else:
                    flash("Please select valid orders.")
                    return redirect('change_status')
            return redirect('change_status')

        elif request.form.get('delete_order') == "delete order":
            orders_li = request.form.getlist('change_stat')
            for i in orders_li:
                db.session.query(order_product).filter_by(order_id=i).delete()
                Order.query.filter_by(id=i).delete()
            return redirect('change_status')


# Registeration page
@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/remove', methods=['GET'])
def remove():
    headings = ("Id", "Name", "Email", "Contact", "Option")
    cus = db.session.query(Customer)
    return render_template('remove.html', headings=headings, customers=cus)


@app.route('/delete_customer', methods=['POST'])
def deletecustomer():
    if request.method == 'POST':
        cu_list = request.form.getlist('culist')
        print(cu_list)
        for i in cu_list:
            if db.session.query(Order).filter_by(customer_id=i).scalar() is not None:
                orderid = db.session.query(Order.id).filter_by(customer_id=i).scalar()
                db.session.query(order_product).filter_by(order_id=orderid).delete()
                db.session.query(Order).filter_by(id=orderid).delete()
                db.session.query(Customer).filter_by(id=i).delete()
            else:
                db.session.query(Customer).filter_by(id=i).delete()

        return remove()


# submitting registration page and redirect to make order
@app.route('/submit', methods=['POST'])
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


@app.route('/add', methods=['GET'])
def add_data():
    if request.method == 'GET':
        return render_template('register.html')


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
        session.clear()
        return render_template('completed.html')


@app.route('/test', methods=['GET'])
def test():
    current_id = str(session.get("value"))
    return current_id
