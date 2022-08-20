import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_mail = os.getenv("MAIL_EMAIL")
mail_pw = os.getenv("MAIL_PW")


class PushMail(object):

    def main(self, recipient, subject, loc):
        message = MIMEMultipart()
        message['From'] = email_mail
        message['To'] = recipient
        message['Subject'] = subject
        f = open(loc, 'r')
        body = f.read()
        message.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
            server.starttls()
            server.login(email_mail, mail_pw)
            text = message.as_string()
            server.sendmail(email_mail, recipient, text)
            # server.quit()
        f.close()

    def welcome(self, recipient):
        loc = r'mailSystem/static/mails/welcome.txt'
        subject = "Welcome"
        self.main(recipient, subject, loc)

    def ordered(self, recipient):
        loc = r'mailSystem/static/mails/ordered.txt'
        subject = "Order Confirmed"
        self.main(recipient, subject, loc)

    def shipped(self, recipient):
        loc = r'mailSystem/static/mails/shipped.txt'
        subject = "Order Shipped"
        self.main(recipient, subject, loc)

    def delivered(self, recipient):
        loc = r'mailSystem/static/mails/delivered.txt'
        subject = "Order Delivered"
        self.main(recipient, subject, loc)

    def pushmails(self, mail_list, subject, content):
        loc = r'mailSystem/static/mails/custom.txt'
        with open(loc, 'w') as f:
            f.write(content)
        for i in mail_list:
            self.main(i, subject, loc)


pushmail = PushMail()
