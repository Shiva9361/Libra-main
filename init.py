from  flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
UPLOAD_FOLDER = r'static'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_database.sqlite3'
app.secret_key = "My_very_secret_key"

db.init_app(app)
app.app_context().push() 