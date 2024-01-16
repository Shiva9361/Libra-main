from flask import render_template,url_for,request,session,redirect
from Classes.Dbmodels import *
from app import app

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
@app.route("/librarian/remove/book/<int:book_id>")
def librarian_remove_book(book_id):
     if "librarian" in session:
          book = Book.query.filter_by(book_id = book_id).first()
          if book is None:
               return render_template("does_not_exist_l.html")
          else:
               db.session.delete(book)
               db.session.commit()
               return redirect(url_for("librarian_dashboard")) 
     return redirect(url_for("librarian_login"))

@app.route("/librarian/revoke/book/<int:book_id>")
def librarian_revoke_book(book_id):
     if "librarian" in session:
          book = Book.query.filter_by(book_id = book_id).first()
          if book is None:
               return render_template("does_not_exist_l.html")
          if book.user_email is None:
               return redirect(url_for("librarian_dashboard"))
          else:
               book.user_email = None
               db.session.add(book)
               db.session.commit()
               return redirect(url_for("librarian_dashboard")) 
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
