from init import app
from flask import render_template,url_for,request,session,redirect,send_from_directory
from Classes.Dbmodels import Book,User,Section,Feedback,Requests,Owner,db,Read
import datetime
"""
User endpoints
"""
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
                    return redirect("/user/home/0")
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
          for book in user.books:
               if book.return_date:
                    if book.return_date < datetime.date.today():
                         return redirect("/user/returnbook/"+str(book.book_id))
          books = Book.query.all()
          ordered_books=[]
          for book in books:
               score = 0
               for feedback in book.feedbacks:
                    score+=feedback.rating
               if len(book.feedbacks)!=0:score/=len(book.feedbacks)
               ordered_books.append((score,book))
          ordered_books.sort(key=lambda x:x[0])
          books = [j for i,j in ordered_books]
          books.reverse()
          sections = Section.query.all()
          return render_template("user_home.html",user_name = user.nick_name,profile = url_for("user_profile"),
                                 ur_books = ur_books,all_books = books,section_present =toggle,
                                 sections = sections,home = True,mail = user_email)
     return redirect(url_for("user_login"))

@app.route("/user/readbook/<string:book_id>")
def read_book(book_id):
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          book = Book.query.filter_by(book_id=book_id).first()
          if book is None:
               return render_template("does_not_exist_u.html",user_name = user.nick_name)
          if user.email == book.user_email:
               if book.file_name:
                    return render_template("read_book.html",user_name = user.nick_name,book = book,url = url_for('static',filename = f"{book.file_name}"))
               return render_template("read_book.html",user_name = user.nick_name,book = book)
          return render_template("access_denied.html",home_url = "/user/home/0")
     return redirect(url_for("user_login"))
@app.route("/user/bookread/<string:book_id>")
def book_read(book_id):
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          book = Book.query.filter_by(book_id=book_id).first()
          if book is None:
               return render_template("does_not_exist_u.html",user_name = user.nick_name)
          for readbook in user.hasread:
               if readbook.book_id == book.book_id:
                    return redirect(f"/user/home/0")
          readbook = Read(user_id = user_email,book_id = book_id,on = datetime.date.today())
          db.session.add(readbook)
          db.session.commit()
          return redirect(f"/user/home/0")
     return redirect(url_for("user_login"))

@app.route("/user/requestbook/<int:book_id>")
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
                    return render_template("request_processing.html",already_requested = True,user_name = user.nick_name)
          if book is None:
               return render_template("does_not_exist_u.html",user_name = user.nick_name)
          request = Requests(user_id = user_email,book_id = book_id,pending = True)
          db.session.add(request)
          db.session.commit()
          return render_template("request_processing.html",user_name = user.nick_name)
     return redirect(url_for("user_login"))

@app.route("/user/returnbook/<int:book_id>")
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

@app.route("/user/feedback/<int:book_id>",methods = ["GET","POST"])
def user_feedback(book_id):
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          if request.method == "POST":
               for i in user.feedbacks:
                    if i.book_id == book_id:
                         return render_template("already_done.html",user_name= user.nick_name)
                    
               rating = request.form["rating"]
               feedback_str = request.form["feedback"]
               feedback = Feedback(
                    book_id = book_id,
                    user_name = user_email,
                    rating = rating,
                    feedback = feedback_str
               )
               db.session.add(feedback)
               db.session.commit()
               return redirect("/user/home/0")
          for i in user.feedbacks:
               if int(i.book_id) == book_id:
                    return render_template("already_done.html",user_name= user.nick_name)
          return render_template("user_feedback.html",user_name =  user.nick_name,book_id = book_id)
     return redirect(url_for("user_login"))

@app.route("/user/home/search/books",methods = ["POST","GET"])
def user_search_books():
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          search_key = '%'+request.form['key']+'%'
          index = request.form['index']
          if index == '1':
               books = Book.query.filter(Book.name.like(search_key)).all()
          else:
               books = Book.query.filter(Book.authors.like(search_key)).all()
          return render_template("user_home_search.html",books = books,key = search_key[1:-1],user_name = user.nick_name)
     return redirect(url_for("root_login"))

@app.route("/user/home/search/sections",methods = ["POST","GET"])
def user_search_sections():
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          search_key = '%'+request.form['key']+'%'
          sections = Section.query.filter(Section.name.like(search_key)).all()
          return render_template("user_home_search.html",sections = sections,key = search_key[1:-1],user_name = user.nick_name)
     return redirect(url_for("root_login"))

@app.route("/user/profile")
def user_profile():
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          read = db.session.query(Book,Read).join(Read, Read.book_id == Book.book_id).filter(Read.user_id==user_email).all()
          return render_template("user_profile.html",user_name = user.nick_name,user=user,books = read)
     return redirect(url_for("root_login"))

@app.route("/user/profile/edit",methods = ["POST","GET"])
def user_profile_edit():
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          if request.method == "POST":
               pname = request.form["pname"]
               fname = request.form["fname"]
               lname = request.form["lname"]
               cno = request.form["cno"]
               about = request.form["about"]
               user.nickname = pname
               user.first_name = fname
               user.last_name = lname
               user.phone_number = cno
               user.about = about
               db.session.add(user)
               db.session.commit()
               return redirect(url_for("user_profile"))
          return render_template("user_profile_edit.html",user = user,user_name = user.nick_name)
     return redirect(url_for("root_login"))
@app.route("/user/buy/<int:book_id>",methods = ["GET","POST"])
def buy_book(book_id):
    if "user" in session:
        user_email = session["user"]
        user = User.query.filter_by(email = user_email).first()
        book = Book.query.filter_by(book_id=book_id).first()
        if book is None:
            return render_template("does_not_exist_u.html",user_name = user.nick_name)
        for i in user.owns:
            if i.book_id == book_id:
                 return redirect(f"/user/download/{book_id}")
        if request.method == "POST":
            owner = Owner(user_email = user_email,book_id = book_id)
            db.session.add(owner)
            db.session.commit()
            return redirect(redirect(f"/user/download/{book_id}"))
        return render_template(f"user_buy_book.html",user_email = user.nick_name,book_id = book_id)
    return redirect(url_for("user_login"))
@app.route("/user/download/<int:book_id>")
def download_book(book_id):
     if "user" in session:
          user_email = session["user"]
          user = User.query.filter_by(email = user_email).first()
          book = Book.query.filter_by(book_id=book_id).first()
          if book is None:
               return render_template("does_not_exist_u.html",user_name = user.nick_name)
          for i in user.owns:
               if i.book_id == book_id:
                    if book.file_name:
                         return send_from_directory(app.config["UPLOAD_FOLDER"],book.file_name)
                    
          return redirect("/user/home/0")
     return redirect(url_for("user_login"))
@app.route("/user/logout")
def user_logout():
     if "user" in session:
          session.pop("user")
          
     return redirect(url_for("user_login"))
