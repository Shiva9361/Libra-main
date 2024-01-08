from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_database.sqlite3'

db = SQLAlchemy()
db.init_app(app)

app.app_context().push()

if __name__ == "__main__":
     app.run(debug = True)