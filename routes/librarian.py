from flask import render_template,url_for,request,session,redirect
from init import app
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import numpy as np 
from Classes.Dbmodels import Book,Section,Requests,Librarian,db
import random
import datetime
import os
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
                    if librarian.check_password(password):
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
          notinuse = len(Book.query.filter_by(user_email = None).all())
          
          values = np.array([notinuse,len(books)-notinuse])
          plt.figure(facecolor='#fffaf0')
          lables = ["Books available","Books with Users"]
          plt.pie(values,labels=lables,startangle=0,autopct="%1.1f%%")
          plt.legend(loc="center")
          plt.savefig("static/chart.png")

          return render_template("librarian_dashboard.html",user_name = user_name,dashboard = True,sections = sections,
                                 books = books)
     return redirect(url_for("librarian_login"))

@app.route("/librarian/requests")
def librarian_requests():
     if "librarian" in session:
          user_name = session["librarian"]
          requests = Requests.query.filter_by(pending = True).all()
          return render_template("librarian_requests.html",requests = requests,user_name = user_name)
     return redirect(url_for("librarian_login"))
@app.route("/librarian/add")
def librarian_add():
     if "librarian" in session:
          user_name = session["librarian"]
          sections = Section.query.all()
          return render_template("librarian_add.html",user_name = user_name,sections = sections)
          
     return redirect(url_for("librarian_login"))
@app.route("/librarian/remove/book/<int:book_id>")
def librarian_remove_book(book_id):
     if "librarian" in session:
          book = Book.query.filter_by(book_id = book_id).first()
          if book is None:
               return render_template("does_not_exist_l.html")
          else:
               for i in book.feedbacks:
                    db.session.delete(i)
               db.session.delete(book)
               db.session.commit()
               return redirect(url_for("librarian_dashboard")) 
     return redirect(url_for("librarian_login"))
@app.route("/librarian/remove/section/<int:section_id>")
def librarian_remove_section(section_id):
     if "librarian" in session:
          section = Section.query.filter_by(section_id = section_id).first()
          if section is None:
               return render_template("does_not_exist_l.html")
          else:
               for book in section.books:
                    book.section_id = 0
                    db.session.add(book)
                    db.session.commit()
               db.session.delete(section)
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

@app.route("/librarian/search/books",methods = ["POST","GET"])
def librarian_search_books():
     if "librarian" in session:
          user_name = session["librarian"]
          search_key = '%'+request.form['key']+'%'
          index = request.form['index']
          if index == '1':
               books = Book.query.filter(Book.name.like(search_key)).all()
          elif index=='3':
               books = Book.query.filter(Book.user_email.like(search_key)).all()
          else:
               books = Book.query.filter(Book.authors.like(search_key)).all()
          section = Section.query.all()
          return render_template("librarian_dashboard.html",books = books,sections = section,user_name = user_name,key_b = search_key[1:-1])
     return redirect(url_for("root_login"))

@app.route("/librarian/search/sections",methods = ["POST","GET"])
def librarian_search_sections():
     if "librarian" in session:
          user_name = session["librarian"]
          search_key = '%'+request.form['key']+'%'
          sections = Section.query.filter(Section.name.like(search_key)).all()
          books = Book.query.all()
          return render_template("librarian_dashboard.html",sections = sections,key_s = search_key[1:-1],user_name = user_name,books = books)
     return redirect(url_for("root_login"))

@app.route("/librarian/add/book",methods=["POST"])
def librarian_add_book():
     if "librarian" in session:
          user_name = session["librarian"]
          file = request.files['content']
          if file :
               if '.' in file.filename and file.filename.split(".")[-1] == "pdf":
                    filename = secure_filename(file.filename)+ request.form["authors"] + str(datetime.date.today())
                    filename = list(filename)
                    random.shuffle(filename)
                    filename = ''.join(filename)+".pdf"
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
                    book = Book(
                         name = request.form["name"],authors = request.form["authors"],
                         section_id = request.form["section_id"],
                         file_name = filename,content = request.form["content1"]
                    )
                    db.session.add(book)
                    db.session.commit()
               else:
                    return render_template("error.html",user_name = user_name,error = "Could not Add")
          else:
               book = Book(
                         name = request.form["name"],authors = request.form["authors"],
                         section_id = request.form["section_id"] if request.form["section_id"] else 0,
                         content = request.form["content1"]
               )
               db.session.add(book)
               db.session.commit()
          return redirect(url_for("librarian_add"))
     return redirect(url_for("librarian_login"))

@app.route("/librarian/modify/book/<int:book_id>",methods=["GET","POST"])
def librarian_modify_book(book_id):
     if "librarian" in session:
          user_name = session["librarian"]
          book = Book.query.filter_by(book_id= book_id).first()
          sections = Section.query.all()
          if book is None:
               return render_template("does_not_exit_l.html",user_name = user_name)
          if request.method == "POST":
               content = request.form["content"]
               authors = request.form["authors"]
               section_id = request.form["section_id"]
               
               book.content = content
               book.authors = authors
               book.section_id = section_id
               db.session.add(book)
               db.session.commit()
               return redirect(url_for("librarian_dashboard"))
          return render_template("librarian_modify_book.html",user_name = user_name,book = book,sections = sections) 
     return redirect(url_for("librarian_login"))

@app.route("/librarian/modify/section/<int:section_id>",methods = ["GET","POST"])
def librarian_modify_section(section_id):
     if "librarian" in session:
          user_name = session["librarian"]
          section = Section.query.filter_by(section_id = section_id).first()
          if section is None:
               return render_template("does_not_exist_l.html",user_name = user_name)
          if request.method == "POST":
               description = request.form["description"]
               section.description = description
               db.session.add(section)
               db.session.commit()
               return redirect(url_for("librarian_dashboard"))
          return render_template("librarian_modify_section.html",user_name = user_name,section = section)
     return redirect(url_for("librarian_login"))

@app.route("/librarian/add/section",methods =["POST"])
def librarian_add_section():
     if "librarian" in session:
          #user_name = session["librarian"]
          section = Section(
               name = request.form["name"],
               description = request.form["description"],
               date_created = datetime.date.today()
          )
          db.session.add(section)
          db.session.commit()

          return redirect(url_for("librarian_add"))
     return redirect(url_for("librarian_login"))

@app.route("/librarian/dashboard/processrequest/<string:request_id>/<int:choice>")
def process_request(choice,request_id):
     if "librarian" in session:
          user_name = session["librarian"]
          if choice == 0:
               _request = Requests.query.filter_by(request_id = request_id).first()
               if _request is None:
                    return redirect(url_for("librarian_dashboard"))
               book = Book.query.filter_by(book_id = _request.book_id).first()
               if book.user_email:
                    return render_template("error_revoke.html",user_name=user_name,book = book)
               #user = User.query.filter_by(email = _request.user_id)
               book.user_email = _request.user_id
               book.issue_date = datetime.date.today()
               book.return_date = datetime.date.today()+ datetime.timedelta(days = 7)
               _request.pending = False
               db.session.add(book)
               db.session.add(_request)
               db.session.commit()
               return redirect(url_for("librarian_requests"))
          elif choice == 1:
               _request = Requests.query.filter_by(request_id = request_id).first()
               if _request is None:
                    return redirect(url_for("librarian_requests"))
               _request.pending = False
               db.session.add(_request)
               db.session.commit()
               return redirect(url_for("librarian_requests"))
          else:
               return redirect(url_for("librarian_dashboard"))
     return redirect(url_for("librarian_login"))

@app.route("/librarian/logout")
def librarian_logout():
     if "librarian" in session:
          session.pop("librarian")

     return redirect(url_for("root_login"))