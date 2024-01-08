from flask import Flask,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_database.sqlite3'

db = SQLAlchemy()
db.init_app(app)

app.app_context().push()

@app.route("/login",methods = ["GET"])
def root_login():
     return render_template("root_login.html",librarian_url = url_for(librarian_login),user_url = url_for(user_login))
"""
Add link to signup
"""
@app.route("/login/user",methods = ["GET","POST"])
def user_login():
     return render_template("user_login.html")
@app.route("/signup/user",methods = ["GET","POST"])
def user_login():
     return render_template("user_login.html")

@app.route("/login/libriarian",methods = ["GET","POST"])
def librarian_login():
     return render_template("librarian_login.html")

@app.route("/login/libriarian/dashboard",methods = ["GET","POST"])
def librarian_login():
     return render_template("librarian_login.html")


@app.route("/login/user/<string:user_id>/home",methods = ["GET","POST"])
def user_home(user_id):
     return render_template("user_login.html")

"""
support update of profile and view
"""
@app.route("/login/user/<string:user_id>/profile",methods = ["GET","POST"])
def user_home(user_id):
     return render_template("user_profile.html")

if __name__ == "__main__":
     app.run(debug = True)