import smtplib
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email import encoders
import os
from dotenv import load_dotenv
from Classes.Dbmodels import VisitHistory, Read, User, Book
from datetime import datetime, timedelta
from flask import render_template
import pdfkit
from init import app, celery

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
        app.config["PRO_UPLOAD_FOLDER"], "reports", filename), configuration=pdf_config)
    return filename


def send_monthly_report(user):
    file = generate_report(user)
    msg = EmailMessage()
    msg["Subject"] = "Your Monthly Report "
    msg["From"] = SENDER
    msg["To"] = user.email
    body = "Attached below is your monthly report for last month"
    msg.set_content(body)
    attach_file_name = os.path.join(
        app.config["PRO_UPLOAD_FOLDER"], 'reports', file)
    attach_file = MIMEApplication(open(attach_file_name, "rb").read())
    attach_file.add_header('Content-Disposition',
                           'attachment', filename=file)
    msg.add_attachment(attach_file)
    with smtplib.SMTP_SSL("smtp.gmail.com") as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(msg)


def send_librarian_report(mail):
    msg = EmailMessage()
    msg["Subject"] = "Async CSV Generation output"
    msg["From"] = SENDER
    msg["To"] = mail
    body = "Attached below is the generated csv file"
    msg.set_content(body)
    attach_file_name = os.path.join(app.config["PRO_UPLOAD_FOLDER"], 'a.csv')
    attach_file = MIMEApplication(open(attach_file_name, "rb").read())
    attach_file.add_header('Content-Disposition',
                           'attachment', filename="output.csv")
    msg.add_attachment(attach_file)
    with smtplib.SMTP_SSL("smtp.gmail.com") as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(msg)


"""
    Celery tasks
"""


@celery.task(name="send_daily_reminder_task")
def send_daily_reminder_task():
    users = VisitHistory.unvisited()
    emails = [(user.email, user.nick_name) for user in users]
    for email, nick_name in emails:
        send_daily_reminder(email, nick_name)


@celery.task(name="send_monthly_report_task")
def send_monthly_report_task():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    if tomorrow.day == 1:  # today is last date
        users = User.query.all()
        for user in users:
            send_monthly_report(user)


@celery.task
def generate_librarian_report(mail):
    books = Book.query.all()
    books = [book.return_data() for book in books]
    with open(f"{app.config['PRO_UPLOAD_FOLDER']}/a.csv", "w") as csvfile:
        csvfile.write(
            "Books\nID,Book Name,Authors,Section Id, User_email,content,issue_date,return_date\n")
        for book in books:
            for data in book.keys():
                csvfile.write(str(book[data])+",")
            csvfile.write("\n")
    send_librarian_report(mail)
