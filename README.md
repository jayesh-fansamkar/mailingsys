
------------


# Customer Mailing system 

The purpose of this project was to create a system that automates sending mails to customers upon account creation and change of order status i.e order shipped, delivered. All while providing you an option to send custom emails to specific selected customers.

For data to operate on - The project also contains a simplified dummy online shopping website which allows you register and place orders.

------------


## installation/deployment 
- you can simply download the project and run it , but before that we will have to create models and insert fake products for customers to place orders.
- once downloaded , go the the project folder , open console/terminal and type the following commands one by one.
 - from mailingsys import  db
 - fom mailingsys import *
 - db.create_all()
 - package1 = Product(name="package1", price="500")
 - package2 = Product(name="package2", price="1000")
 - db.session.add(package1)
 - db.session.add(package2)
 - db.session.commit()
-  once done simply run the app and you are good to go.
------------
## thank-you 

------------
