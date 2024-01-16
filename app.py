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




if __name__ == "__main__":
     app.run(debug = True)