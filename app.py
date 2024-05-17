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
    return redirect(url_for("root_login"))


@app.route("/login", methods=["GET"])
def root_login():
    return render_template("root_login.html", librarian_url=url_for('librarian_login'), user_url=url_for('user_login'))


@celery.task(name="send_daily_reminder_task")
def send_daily_reminder_task():
    send_daily_reminder("shivadharshansankar936@gmail.com", "gg")


if __name__ == "__main__":
    app.run(debug=True)
