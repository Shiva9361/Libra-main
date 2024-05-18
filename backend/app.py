from flask import render_template, url_for, redirect
from Classes.Dbmodels import *
from init import app, celery
from routes.user import *
from routes.librarian import *
from Classes.api import *
from jobs import send_daily_reminder

celery.conf.beat_schedule = {
    'daily_remainder': {
        'task': 'send_daily_reminder_task',
        'schedule': 30  # crontab(hour=17, minute=30)
    }
}


@app.route('/')
def index():
    return render_template("index.html")


@celery.task(name="send_daily_reminder_task")
def send_daily_reminder_task():
    send_daily_reminder("shivadharshansankar936@gmail.com", "gg")


if __name__ == "__main__":
    app.run(debug=True)
