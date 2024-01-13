from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    nick_name = db.Column(db.String(30),nullable = False)
    user_pass = db.Column(db.String(20),nullable = False)
    first_name = db.Column(db.String(30),nullable = False)
    last_name = db.Column(db.String(30))
    phone_number = db.Column(db.String(10),nullable = False)
    email = db.Column(db.String,primary_key = True)
    requests = db.relationship('request',backref='user')
    #about = db.Column(db.String)

class Librarian(db.Model):
    __tablename__ = "librarian"
    user_name = db.Column(db.String,primary_key = True)
    password = db.Column(db.String,nullable = False)

class Book(db.Model):
    __tablename__ = "Book"
    book_id = db.Column(db.String,primary_key = True)
    name = db.Column(db.String,nullable = False)
    content = db.Column(db.String,nullable = False)
    authors = db.Column(db.String,nullable = False)
    issue_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    section_id = db.Column(db.String,db.ForeignKey("Section.section_id"),nullable = False)
    feedbacks = db.relationship("feedback",backref = "Book")

class Section(db.Model):
    __tablename__ = "Section"
    section_id = db.Column(db.String,primary_key = True)
    name = db.Column(db.String,nullable = False)
    date_created = db.Column(db.Date,nullable = False)
    description = db.Column(db.String,nullable = False)

class Feedback(db.Model):
    __tablename__ = "Feedback"
    feedback_id = db.Column(db.String,primary_key = True)
    book_id = db.Column(db.String,db.ForeignKey("Book.book_id"),nullable = False)
    user_name = db.Column(db.String,db.ForeignKey("user.email"),nullable = False)
    rating = db.Column(db.Integer,nullable = False)
    feedback = db.Column(db.String,nullable = False)

class Requests(db.Model):
    __tablename__ = "Requests"
    request_id = db.Column(db.Integer,autoincrement = True,primary_key = True)
    user_id = db.Column(db.String,db.ForeignKey('user.email'),nullable = False)
    book_id = db.Column(db.String,db.ForeignKey('Book.book_id'),nullable = False)
    pending = db.Column(db.Boolean,default = True)

