from flask import Flask,render_template,url_for,request,session,redirect
from Classes.Dbmodels import *
#from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_database.sqlite3'
app.secret_key = "My_very_secret_key"
"""app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"""
#Session(app)
db.init_app(app)
app.app_context().push() 

@app.route('/')
def index():
     return redirect(url_for("root_login"))

@app.route("/login",methods = ["GET"])
def root_login():
     return render_template("root_login.html",librarian_url = url_for('librarian_login'),user_url = url_for('user_login'))

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
               return render_template("does_not_exist.html",home = url_for("home"))
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
               return render_template("does_not_exist.html",home = "/user/home/0")
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

"""
Librarian endpoints
"""

@app.route("/login/librarian",methods = ["GET","POST"])
def librarian_login():
     if "librarian" in session:
          return redirect(url_for("librarian_dashboard"))
     else:
          if request.method=="POST":
               user_name = request.form["uname"]
               password = request.form["upass"]
               librarian = Librarian.query.filter_by(user_name = user_name).first()

               if not librarian:
                    return render_template("librarian_login.html",udne = True,wrong_pass= False)
               else:
                    if librarian.password == password:
                         session["librarian"] = user_name
                         return redirect(url_for("librarian_dashboard"))
                    else:
                         return render_template("librarian_login.html",udne = False,wrong_pass= True,user_name = user_name)

     return render_template("librarian_login.html",udne = False,wrong_pass= False)

@app.route("/librarian/dashboard",methods = ["GET","POST"])
def librarian_dashboard():
     if "librarian" in session:
          user_name = session["librarian"]
          sections = Section.query.all()
          books = Book.query.all()
          return render_template("librarian_dashboard.html",user_name = user_name,dashboard = True,sections = sections,
                                 books = books)
     return redirect(url_for("librarian_login"))

@app.route("/librarian/requests")
def librarian_requests():
     if "librarian" in session:
          user_name = session["librarian"]
          requests = Requests.query.all()
          return render_template("librarian_requests.html",requests = requests,user_name = user_name)
     return redirect(url_for("librarian_login"))
@app.route("/librarian/add")
def librarian_add():
     if "librarian" in session:
          user_name = session["librarian"]
          return render_template("librarian_add.html",user_name = user_name)
          
     return redirect(url_for("librarian_login"))


@app.route("/librarian/add/book",methods=["POST"])
def librarian_add_book():
     if "librarian" in session:
          #user_name = session["librarian"]
          book = Book(
               name = request.form["name"],content = request.form["content"],
               authors = request.form["authors"],section_id = request.form["section_id"]
          )
          db.session.add(book)
          db.session.commit()
          return redirect(url_for("librarian_add"))
     return redirect(url_for("librarian_login"))

@app.route("/librarian/add/section",methods =["POST"])
def librarian_add_section():
     if "librarian" in session:
          #user_name = session["librarian"]
          section = Section(
               name = request.form["name"],
               description = request.form["description"]
          )
          db.session.add(section)
          db.session.commit()

          return redirect(url_for("librarian_add"))
     return redirect(url_for("librarian_login"))

@app.route("/librarian/dashboard/processrequest/<string:request_id>/<int:choice>")
def process_request(choice,request_id):
     if "librarian" in session:
          #user_name = session["librarian"]
          if choice == 0:
               _request = Requests.query.filter_by(request_id = request_id).first()
               if _request is None:
                    return redirect(url_for("librarian_dashboard"))
               book = Book.query.filter_by(book_id = _request.book_id).first()
               #user = User.query.filter_by(email = _request.user_id)
               book.user_email = _request.user_id
               _request.pending = False
               db.session.add(book)
               db.session.add(_request)
               db.session.commit()
               return redirect(url_for("librarian_dashboard"))
          elif choice == 1:
               _request = Requests.query.filter_by(request_id = request_id).first()
               if _request is None:
                    return redirect(url_for("librarian_dashboard"))
               _request.pending = False
               db.session.add(_request)
               db.session.commit()
               
          else:
               return redirect(url_for("librarian_dashboard"))
@app.route("/librarian/logout")
def librarian_logout():
     if "librarian" in session:
          session.pop("librarian")
          return redirect(url_for("librarian_login"))
     return redirect(url_for("librarian_login"))


if __name__ == "__main__":
     app.run(debug = True)