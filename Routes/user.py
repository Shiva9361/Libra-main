from app import app
from flask import render_template,url_for,request,session,redirect
from Classes.Dbmodels import *

@app.route("/login/user",methods = ["GET","POST"])
def user_login():
     if "user" in session:
          user_email = session["user"]
          return redirect("/user/home/1")
     if request.method == "POST":
          user_email = request.form['uemail']
          user_pass = request.form['upass']

          user = User.query.filter_by(email = user_email).first()
          if user is None:
               return render_template("user_login.html",wrong_pass = False,udne = True,create_account_url = url_for("user_create"))
          else:
               if user.user_pass == user_pass:
                    session["user"] = user_email
                    return redirect("/user/home/1")
               return render_template("user_login.html",wrong_pass = True,udne = False,create_account_url = url_for("user_create"),email = user_email)
               
     return render_template("user_login.html",wrong_pass = False,udne = False,create_account_url = url_for("user_create"))

@app.route("/signup/user",methods = ["GET","POST"])
def user_create():
     if request.method == "POST":
          user_email = request.form['email']
          first_name = request.form['fname']
          last_name = request.form['lname']
          pnum = request.form['pnum']
          nick_name = request.form['nick_name']
          user_pass = request.form['user_pass']
          
          user = User.query.filter_by(email = user_email).first()
          
          if user is None:
               new_user = User(nick_name = nick_name,user_pass = user_pass,
                               first_name = first_name, last_name = last_name,
                               phone_number = pnum,email = user_email
                               )
               db.session.add(new_user)
               db.session.commit()
               return redirect(url_for('user_login'))
          else:
               return render_template("user_signup.html",email = True,nick_name = nick_name,user_pass = user_pass,
                               first_name = first_name, last_name = last_name,
                               phone_number = pnum)

     return render_template("user_signup.html",email = False,data = "")

@app.route("/user/home/<int:toggle>")
def user_home(toggle):
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          ur_books = user.books
          books = Book.query.all()
          sections = Section.query.all()
          return render_template("user_home.html",user_name = user.nick_name,profile = url_for("user_profile"),
                                 ur_books = ur_books,all_books = books,section_present =toggle,
                                 sections = sections,home = True)
     return redirect(url_for("user_login"))

@app.route("/user/readbook/<string:book_id>")
def read_book(book_id):
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          book = Book.query.filter_by(book_id=book_id).first()
          if book is None:
               return render_template("does_not_exist_u.html",home = url_for("home"))
          if user.email == book.user_email:
               return render_template("read_book.html",book = book,user_name = user.nick_name)
          return render_template("access_denied.html",home_url = "/user/home/0")
     return redirect(url_for("user_login"))

@app.route("/user/requestbook/<string:book_id>")
def request_book(book_id):
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          book = Book.query.filter_by(book_id=book_id).first()
          found = False
          requests = user.requests
          for i in user.books:
               if (i.book_id==book_id):
                    found = True
          if found:
               return redirect(f"/user/readbook/{book.book_id}")
          if len(user.books) >=5:
               return render_template("max_present.html",user_name = user.nick_name)
          for i in requests:
               if i.book_id == book.book_id and i.pending:
                    return render_template("request_processing.html",home = "/user/home/0",already_requested = True)
          if book is None:
               return render_template("does_not_exist_u.html",home = "/user/home/0")
          request = Requests(user_id = user_email,book_id = book_id,pending = True)
          db.session.add(request)
          db.session.commit()
          return render_template("request_processing.html",home = "/user/home/0")
     return redirect(url_for("user_login"))

@app.route("/user/returnbook/<string:book_id>")
def return_book(book_id):
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          found = False
          for book in user.books:
               if book.book_id == book_id:
                    found=True
                    break
          if found:
               book = Book.query.filter_by(book_id = book_id).first()
               book.user_email = None
               db.session.add(book)
               db.session.commit()
               return redirect("/user/home/0")
          return redirect("/user/home/0")
          
     return redirect(url_for("user_login"))
@app.route("/user/home/search/books",methods = ["POST","GET"])
def user_search_books():
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          search_key = '%'+request.form['key']+'%'
          books = Book.query.filter(Book.name.like(search_key)).all()
          return render_template("user_home_search.html",books = books,key = search_key[1:-1],user_name = user.nick_name)
     return redirect(url_for("user_login"))

@app.route("/user/home/search/sections",methods = ["POST","GET"])
def user_search_sections():
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          search_key = '%'+request.form['key']+'%'
          sections = Section.query.filter(Section.name.like(search_key)).all()
          return render_template("user_home_search.html",sections = sections,key = search_key[1:-1],user_name = user.nick_name)
     return redirect(url_for("user_login"))

@app.route("/user/profile")
def user_profile():
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          return render_template("user_profile.html",user_name = user.nick_name,user=user)
     return redirect(url_for("user_login"))

@app.route("/user/profile/edit")
def user_profile_edit():
     return render_template("user_profile_edit.html")

@app.route("/user/logout")
def user_logout():
     if "user" in session:
          session.pop("user")
          return redirect(url_for("user_login"))
     return redirect(url_for("user_login"))
