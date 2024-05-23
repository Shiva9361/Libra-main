import smtplib
from email.message import EmailMessage
import os

SENDER = "22f3001421@ds.study.iitm.ac.in"
PASSWORD = os.environ["password"] if "password" in os.environ else ""


def send_daily_reminder(email, username):
    msg = EmailMessage()
    msg["Subject"] = "Login Reminder"
    msg["From"] = SENDER
    msg["To"] = email
    body = "This is your reminder to visit Libra !! \nSo many books waiting to be read\n\n\nThis is a auto generated text, Please Don't Reply"
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com") as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(msg)
