from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    user_name = db.Column(db.String,primary_key = True)
    user_pass = db.Column(db.String,nullable = False)
    first_name = db.Column(db.String,nullable = False)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String,nullable = False)
    email = db.Column(db.String,nullable = False)

class Librarian(db.Model):
    __tablename__ = "librarian"
    librarian_user_name = db.Column(db.String,primary_key = True)
    librarian_pass = db.Column(db.String,nullable = False)

class Book(db.Model):
    __tablename__ = "Book"
    book_id = db.Column(db.String,primary_key = True)
    name = db.Column(db.String,nullable = False)
    content = db.Column(db.String,nullable = False)
    authors = db.Column(db.String,nullable = False)
    issue_date = db.Column(db.Date)
    return_date = db.Column(db.Date)

class Section(db.Model):
    __tablename__ = "Section"
    section_id = db.Column(db.String,primary_key = True)
    name = db.Column(db.String,nullable = False)
    date_created = db.Column(db.Date,nullable = False)
    description = db.Column(db.String,nullable = False)
