import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from Classes.Dbmodels import User, VisitHistory, Requests, Read
from datetime import datetime, timedelta, date
from flask import render_template
import pdfkit
from init import app
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
    books_read = Read.query.filter(Read.user_id == user.email,
                                   Read.on >= start_date, Read.on <= end_date).all()
    books_read = [read.book.return_data() for read in books_read]
    number_of_books_read = len(books_read)
    pdf_template = render_template("report_template.html", date=end_date.date(), user=user,
                                   number_of_days=number_of_days, books_read=number_of_books_read, books=books_read)
    filename = user.nick_name+str(end_date.date())+".pdf"
    pdf_config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    pdfkit.from_string(pdf_template, os.path.join(
        app.config["UPLOAD_FOLDER"], "reports", filename), configuration=pdf_config)
    return filename


def send_monthly_report(user):
    file = generate_report(user)
    msg = EmailMessage()
    msg["Subject"] = "Your Monthly Report "
    msg["From"] = SENDER
    msg["To"] = user.email
    body = "Attached below is your monthly report for last month"
    msg.set_content(body)
    msg.add_attachment(os.path.join(
        app.config["UPLOAD_FOLDER"], "reports", file))
    # with smtplib.SMTP_SSL("smtp.gmail.com") as smtp:
    #     smtp.login(SENDER, PASSWORD)
    #     smtp.send_message(msg)
