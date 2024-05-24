from flask import request, jsonify
from init import app
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import numpy as np
from Classes.Dbmodels import Book, Section, Requests, Librarian, db
import random
import datetime
import jwt
import os
from functools import wraps
"""
Librarian endpoints
"""


def token_required(fun):
    @wraps(fun)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms="HS256")
            if data['role'] != "librarian":
                return jsonify(invalid_msg), 401
            librarian = Librarian.query.filter_by(email=data['email']).first()
            if not librarian:
                raise RuntimeError('Librarian not found')
            return fun(librarian, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@app.route("/login/librarian", methods=["GET", "POST"])
def librarian_login():
    data = request.get_json()
    user_name = data.get("uname")
    password = data.get("upass")
    librarian = Librarian.query.filter_by(user_name=user_name).first()

    if not librarian:
        return {"error": "Record does not exist"}, 404
    else:
        if librarian.check_password(password):
            token = jwt.encode({
                'email': Librarian.user_name,
                'exp': (datetime.datetime.now()+datetime.timedelta(minutes=30)).strftime("%s"),
                'role': "librarian",
            }, app.config['SECRET_KEY'])

            return jsonify({'token': token, 'user_details': librarian.return_data()}), 200
    return {"error": "wrong password"}, 403


@app.route("/librarian/dashboard", methods=["GET", "POST"])
@token_required
def librarian_dashboard(librarian):
    sections = Section.query.all()
    sections = [section.return_data() for section in sections]
    books = Book.query.all()
    books = [book.return_data() for book in sections]
    notinuse = len(Book.query.filter_by(user_email=None).all())

    values = np.array([notinuse, len(books)-notinuse])
    plt.figure(facecolor='#fffaf0')
    lables = ["Books available", "Books with Users"]
    plt.pie(values, labels=lables, startangle=0, autopct="%1.1f%%")
    plt.legend(loc="center")
    plt.savefig("static/chart.png")

    return jsonify(dict(user_name=librarian.user_name, sections=sections,
                        books=books)), 200


@app.route("/librarian/remove/book/<int:book_id>")
@token_required
def librarian_remove_book(librarian, book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        return {"error": "book does not exist"}, 404
    else:
        for i in book.feedbacks:
            db.session.delete(i)
        db.session.delete(book)
        db.session.commit()
        return {"message": "done"}, 200


@app.route("/librarian/remove/section/<int:section_id>")
@token_required
def librarian_remove_section(librarian, section_id):
    section = Section.query.filter_by(section_id=section_id).first()
    if section is None:
        return {"error", "section does not exist"}, 404

    for book in section.books:
        book.section_id = 0
        db.session.add(book)
        db.session.commit()
    db.session.delete(section)
    db.session.commit()
    return {"message": "done"}, 200


@app.route("/librarian/revoke/book/<int:book_id>")
@token_required
def librarian_revoke_book(librarina, book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        return {"error": "book does not exist"}, 404
    if book.user_email is None:
        return {"error": "no one has the book"}, 404
    book.user_email = None
    db.session.add(book)
    db.session.commit()
    return {"message": "done"}, 200


@app.route("/librarian/search/books", methods=["POST"])
@token_required
def librarian_search_books(librarian):

    data = request.get_json()
    search_key = '%'+data.get('key')+'%'
    index = data.get('index')
    if index == '1':
        books = Book.query.filter(Book.name.like(search_key)).all()
    elif index == '3':
        books = Book.query.filter(Book.user_email.like(search_key)).all()
    else:
        books = Book.query.filter(Book.authors.like(search_key)).all()
    books = [book.return_data() for book in books]
    return jsonify(books), 200


@app.route("/librarian/search/sections", methods=["POST"])
@token_required
def librarian_search_sections(librarian):
    search_key = '%'+request.form['key']+'%'
    sections = Section.query.filter(Section.name.like(search_key)).all()
    sections = [section.return_data() for section in sections]
    return jsonify(sections), 200


@app.route("/librarian/add/book", methods=["POST"])
@token_required
def librarian_add_book(librarian):
    file = request.files['content']
    if file:
        if '.' in file.filename and file.filename.split(".")[-1] == "pdf":
            filename = secure_filename(
                file.filename) + request.form["authors"] + str(datetime.date.today())
            filename = list(filename)
            random.shuffle(filename)
            filename = ''.join(filename)+".pdf"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            book = Book(
                name=request.form["name"], authors=request.form["authors"],
                section_id=request.form["section_id"],
                file_name=filename, content=request.form["content1"]
            )
            db.session.add(book)
            db.session.commit()
            return {"message": "done"}, 200
        else:
            return {"error": "could not add"}
        """
        should generate pdfs
        """
    book = Book(
        name=request.form["name"], authors=request.form["authors"],
        section_id=request.form["section_id"] if request.form["section_id"] else 0,
        content=request.form["content1"]
    )
    db.session.add(book)
    db.session.commit()
    return {"message": "done"}, 200


@app.route("/librarian/modify/book/<int:book_id>", methods=["POST"])
@token_required
def librarian_modify_book(librarian, book_id):

    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        return {"error": "book does not exist"}, 404
    data = request.get_json()

    if name == "" or authors == "" or section_id == "":
        return {"error": "some fields are empty"}
    name = data.get("name")
    content = data.get("content")
    authors = data.get("authors")
    section_id = data.get("section_id")
    book.content = content
    book.authors = authors
    book.section_id = section_id
    db.session.add(book)
    db.session.commit()
    return {"message": "done"}, 200


@app.route("/librarian/modify/section/<int:section_id>", methods=["POST"])
@token_required
def librarian_modify_section(librarian, section_id):
    section = Section.query.filter_by(section_id=section_id).first()
    if section is None:
        return {"error": "section does not exist"}, 404
    data = request.get_json()
    description = data.get("description")
    name = data.get("name")
    if description == "" or name == "":
        return {"error": "some fields are empty"}
    section.description = description
    section.name = name
    db.session.add(section)
    db.session.commit()
    return {"message": "done"}, 200


@app.route("/librarian/add/section", methods=["POST"])
@token_required
def librarian_add_section(librarian):
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    if name == "" or description == "":
        return {"error": "some fields are empty"}
    section = Section(
        name=name,
        description=description,
        date_created=datetime.date.today()
    )
    db.session.add(section)
    db.session.commit()

    return {"message": "done"}


@app.route("/librarian/dashboard/processrequest/<string:request_id>/<int:choice>")
@token_required
def process_request(librarian, choice, request_id):
    if choice == 0:
        _request = Requests.query.filter_by(request_id=request_id).first()
        if _request is None:
            return {"error": "request does not exist"}, 404
        book = Book.query.filter_by(book_id=_request.book_id).first()
        if book.user_email:
            return jsonify(dict(book=book.return_data(), with_user=True))

        book.user_email = _request.user_id
        book.issue_date = datetime.date.today()
        book.return_date = datetime.date.today() + datetime.timedelta(days=7)
        _request.pending = False
        db.session.add(book)
        db.session.add(_request)
        db.session.commit()
        return {"message": "done"}, 200
    elif choice == 1:
        _request = Requests.query.filter_by(request_id=request_id).first()
        if _request is None:
            return {"error": "request does not exist"}, 404
        _request.pending = False
        db.session.add(_request)
        db.session.commit()
        return {"message": "done"}, 200
    return {"error": "invalid choice"}
