from flask import render_template,url_for,redirect
from Classes.Dbmodels import *
from init import app
from routes.user import *
from routes.librarian import *
from Classes.api import *

@app.route('/')
def index():
     return redirect(url_for("root_login"))

@app.route("/login",methods = ["GET"])
def root_login():
     return render_template("root_login.html",librarian_url = url_for('librarian_login'),user_url = url_for('user_login'))

if __name__ == "__main__":
     app.run(debug = True)