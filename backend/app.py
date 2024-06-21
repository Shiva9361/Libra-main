from flask import render_template
from Classes.Dbmodels import *
from init import app, celery, socketio
from routes.user import *
from routes.librarian import *
from Classes.api import *
from jobs import send_daily_reminder, send_monthly_report
from celery.schedules import crontab
from datetime import timedelta

celery.conf.beat_schedule = {
    'daily_remainder': {
        'task': 'send_daily_reminder_task',
        'schedule': crontab(hour=16, minute=30)  # 4:30 daily
    }
}

celery.conf.beat_schedule = {
    'monthly_report': {
        'task': 'send_monthly_report_task',
        'schedule': crontab(day_of_month='28-31', hour=23, minute=0)
    }
}


@app.route('/')
def index():
    return render_template("index.html")


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
    socketio.run(app, debug=True)
