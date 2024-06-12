from flask import render_template, url_for, redirect
from Classes.Dbmodels import *
from init import app, celery
from routes.user import *
from routes.librarian import *
from Classes.api import *
from jobs import send_daily_reminder
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

celery.conf.beat_schedule = {
    'daily_remainder': {
        'task': 'send_daily_reminder_task',
        'schedule': crontab(hour=16, minute=30)  # 4:30 daily
    }
}


@app.route('/')
def index():
    return render_template("index.html")


@celery.task(name="send_daily_reminder_task")
def send_daily_reminder_task():
    users = VisitHistory.unvisited()
    emails = [(user.email, user.nick_name) for user in users]
    for email, nick_name in emails:
        send_daily_reminder(email, nick_name)


if __name__ == "__main__":
    if not os.path.exists("instance/library_database.sqlite3"):
        db.create_all()
        librarian = Librarian(
            user_name=os.environ["LIBRARIAN_USERNAME"])
        librarian.set_password(os.environ["LIBRARIAN_PASS"])
        section = Section(section_id=0, name="Default",
                          description="Default section", date_created=datetime.datetime.now())
        db.session.add(librarian)
        db.session.add(section)
        db.session.commit()
    app.run(debug=True)
