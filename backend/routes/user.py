from init import app
from flask import render_template, url_for, request, session, redirect, send_from_directory, jsonify
from Classes.Dbmodels import Book, User, Section, Feedback, Requests, Owner, db, Read
import datetime
import jwt
from functools import wraps
"""
User endpoints
"""


def token_required(fun):
    @wraps(fun)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        print(auth_headers)
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
            if data['role'] != "user":
                return jsonify(invalid_msg), 401
            user = User.query.filter_by(email=data['email']).first()
            if not user:
                raise RuntimeError('User not found')
            return fun(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@app.route("/login/user", methods=["POST"])
def user_login():

    data = request.get_json()
    user = User.validate(**data)
    if user is None:
        return jsonify({'error': 'Invalid Credentials', 'authenticated': False}), 401

    token = jwt.encode({
        'email': user.email,
        'expiry': (datetime.datetime.utcnow()+datetime.timedelta(minutes=30)).strftime("%s"),
        'role': "user",
    }, app.config['SECRET_KEY'])

    return jsonify({'token': token, 'user_details': user.return_data()}), 200


@app.route("/signup/user", methods=["POST"])
def user_create():
    data = request.get_json()
    user_email = data.get('email')
    first_name = data.get('fname')
    last_name = data.get('lname')
    pnum = data.get('pnum')
    nick_name = data.get('nick_name')
    user_pass = data.get('password')

    user = User.query.filter_by(email=user_email).first()
    if user is None:
        new_user = User(nick_name=nick_name,
                        first_name=first_name, last_name=last_name,
                        phone_number=pnum, email=user_email
                        )
        new_user.set_password(user_pass)
        db.session.add(new_user)
        db.session.commit()
        return new_user.return_data(), 201

    return {"error": "Could Not Create"}, 401


@app.route("/user/readbook/<string:book_id>")
def read_book(book_id):
    if "user" in session:
        user_email = session["user"]
        user = User.query.filter_by(email=user_email).first()
        book = Book.query.filter_by(book_id=book_id).first()
        if book is None:
            return render_template("does_not_exist_u.html", user_name=user.nick_name)
        if user.email == book.user_email:
            if book.file_name:
                return render_template("read_book.html", user_name=user.nick_name, book=book, url=url_for('static', filename=f"{book.file_name}"))
            return render_template("read_book.html", user_name=user.nick_name, book=book)
        return render_template("access_denied.html", home_url="/user/home/0")
    return redirect(url_for("user_login"))


@app.route("/user/books", methods=["GET"])
@token_required
def all_books(user):
    books = Book.query.all()
    ordered_books = []
    for book in books:
        score = 0
        for feedback in book.feedbacks:
            score += feedback.rating
            if len(book.feedbacks) != 0:
                score /= len(book.feedbacks)
            ordered_books.append((round(score, 2), book))
    ordered_books.sort(key=lambda x: x[0])
    ordered_books.reverse()
    response = []
    for rating, book in ordered_books:
        temp = book.return_data()
        temp["rating"] = rating
        response.append(temp)
    return jsonify(response), 201


@app.route("/user/bookread/<string:book_id>", methods=["GET"])
@token_required
def book_read(user, book_id):

    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        return {"error": "Book does not exist"}, 401
    if book.user_email != user.email:
        return {"error": "No Access"}, 401
    for readbook in user.hasread:
        if int(readbook.book_id) == book.book_id:
            return {"error": "Already marked as read"}, 401
    readbook = Read(user_id=user.email, book_id=book_id,
                    on=datetime.date.today())
    db.session.add(readbook)
    db.session.commit()
    return {"message": "Done"}, 201


@app.route("/user/requestbook/<int:book_id>", methods=["GET"])
@token_required
def request_book(user, book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    found = False
    requests = user.requests
    for i in user.books:
        if (int(i.book_id) == book_id):
            found = True
    if found:
        return {"message": "Already in Possession"}, 201
    if len(user.books) >= 5:
        return {"error": "Max Books in Possession"}, 401
    for i in requests:
        if int(i.book_id) == book.book_id and int(i.pending):
            return {"message": "Already Requested"}, 201
    if book is None:
        return {"error": "Book does not exist"}, 401
    request = Requests(user_id=user.email, book_id=book_id, pending=True)
    db.session.add(request)
    db.session.commit()
    return {"message": "Requested"}, 201


@app.route("/user/returnbook/<int:book_id>", methods=["POST"])
@token_required
def return_book(user, book_id):
    found = False
    for book in user.books:
        if int(book.book_id) == book_id:
            found = True
            break
    if found:
        book = Book.query.filter_by(book_id=book_id).first()
        book.user_email = None
        db.session.add(book)
        db.session.commit()
        return {"message": "returned"}, 201

    return {"error": "Not able to process"}, 401


@app.route("/user/feedback/<int:book_id>", methods=["POST"])
@token_required
def user_feedback(user, book_id):
    for i in user.feedbacks:
        if int(i.book_id) == book_id:
            return {"error": "Already Given"}, 401

    rating = request.form["rating"]
    feedback_str = request.form["feedback"]
    feedback = Feedback(
        book_id=book_id,
        user_name=user.email,
        rating=rating,
        feedback=feedback_str
    )
    db.session.add(feedback)
    db.session.commit()
    return {"message": "Feedback registered"}, 201


@app.route("/user/home/search/books", methods=["POST"])
@token_required
def user_search_books(user):
    data = request.get_json()
    search_key = '%'+data.get('key')+'%'
    index = data.get('index')
    if index == '1':
        books = Book.query.filter(Book.name.like(search_key)).all()
    else:
        books = Book.query.filter(Book.authors.like(search_key)).all()
    return jsonify({"books": books, "key": search_key[1:-1], "user_name": user.nick_name}), 201


@app.route("/user/home/search/sections", methods=["POST", "GET"])
def user_search_sections():
    if "user" in session:
        user_email = session["user"]
        user = User.query.filter_by(email=user_email).first()
        search_key = '%'+request.form['key']+'%'
        sections = Section.query.filter(Section.name.like(search_key)).all()
        return render_template("user_home_search.html", sections=sections, key=search_key[1:-1], user_name=user.nick_name)
    return redirect(url_for("root_login"))


@app.route("/user/profile", methods=["GET"])
@token_required
def user_profile(user):
    data = db.session.query(Book, Read).join(
        Read, Read.book_id == Book.book_id).filter(Read.user_id == user.email).all()
    books = []
    for book, read in data:
        temp = book.return_data()
        temp["on"] = read.on
        books.append(temp)
    return jsonify({"user_name": user.nick_name, "user": user.return_data(), "books": books}), 201


@app.route("/user/profile/edit", methods=["POST"])
@token_required
def user_profile_edit(user):
    data = request.get_json()
    pname = data.get("pname")
    fname = data.get("fname")
    lname = data.get("lname")
    cno = data.get("cno")
    about = data.get("about")
    user.nick_name = pname
    user.first_name = fname
    user.last_name = lname
    user.phone_number = cno
    user.about = about
    db.session.add(user)
    db.session.commit()
    return {"message": "done"}, 200


@app.route("/user/buy/<int:book_id>", methods=["GET", "POST"])
def buy_book(book_id):
    if "user" in session:
        user_email = session["user"]
        user = User.query.filter_by(email=user_email).first()
        book = Book.query.filter_by(book_id=book_id).first()
        if book is None:
            return render_template("does_not_exist_u.html", user_name=user.nick_name)
        for i in user.owns:
            if int(i.book_id) == book_id:
                return redirect(f"/user/download/{book_id}")
        if request.method == "POST":
            owner = Owner(user_email=user_email, book_id=book_id)
            db.session.add(owner)
            db.session.commit()
            return redirect(f"/user/download/{book_id}")
        return render_template(f"user_buy_book.html", user_name=user.nick_name, book_id=int(book_id))
    return redirect(url_for("user_login"))


@app.route("/user/checkfeedback/<int:book_id>")
def check_feedback(book_id):
    if "user" in session:
        user_email = session["user"]
        user = User.query.filter_by(email=user_email).first()
        feedbacks = Feedback.query.filter_by(book_id=book_id)
        return render_template("feedback.html", user_name=user.nick_name, feedbacks=feedbacks)
    return redirect(url_for("user_login"))


@app.route("/user/download/<int:book_id>")
def download_book(book_id):
    if "user" in session:
        user_email = session["user"]
        user = User.query.filter_by(email=user_email).first()
        book = Book.query.filter_by(book_id=book_id).first()
        if book is None:
            return render_template("does_not_exist_u.html", user_name=user.nick_name)
        for i in user.owns:
            if int(i.book_id) == book_id:
                if book.file_name:
                    return send_from_directory(app.config["UPLOAD_FOLDER"], book.file_name)

        return redirect("/user/home/0")
    return redirect(url_for("user_login"))


@app.route("/user/logout")
def user_logout():
    if "user" in session:
        session.pop("user")

    return redirect(url_for("user_login"))
