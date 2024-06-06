import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from Classes.Dbmodels import User, VisitHistory, Requests, Read
from datetime import datetime, timedelta, date
load_dotenv()
SENDER = os.environ["EMAIL"] if "EMAIL" in os.environ else ""
PASSWORD = os.environ["PASSWORD"] if "PASSWORD" in os.environ else ""


def send_daily_reminder(email, username):
    msg = EmailMessage()
    msg["Subject"] = "Login Reminder"
    msg["From"] = SENDER
    msg["To"] = email
    body = f"Hello {username},\nThis is your reminder to visit Libra !! \nSo many books waiting to be read\n\n\nThis is a auto generated text, Please Don't Reply"
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com") as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(msg)


def generate_report(user):
    year = datetime.now().year
    month = datetime.now().month
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month+1, 1) + timedelta(days=-1)\
        if month != 12 else datetime(year, month, 31)
    number_of_days = len(VisitHistory.query.filter(VisitHistory.user_id ==
                         user.email, VisitHistory.on >= start_date, VisitHistory.on <= end_date).all())
    books_read = len(Read.query.filter(Read.user_id == user.email,
                     Read.on >= start_date, Read.on <= end_date).all())


generate_report(User.query.filter_by(email="testtt@gmail.com").first())
