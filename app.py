from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import hashlib
import sqlite3

app = Flask(__name__)
# Session: user-specific (from session) data is used
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# -----------Hier stehen die gewünschten Funktionen----------------
@app.route("/")
@login_required
def index():
    """show the portfolio of stocks"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in user"""

    #Forget any user_id
    session.clear()

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # user submitting data (logging in)
    if request.method == "POST":
        #check if username is valid
        if not request.form.get("username"):
            return apology("must provide username")
        #check if password is valid
        elif not request.form.get("password"):
            return apology("must provide password")

        # check for corresponding username in database (placeholder!)
        rows = c.execute("SELECT * WHERE username = :username", {'username': request.form.get("username")}).fetchall()

        



# -----------Hier stehen die gewünschten Funktionen----------------

@app.route("/users")
def users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    rows = c.execute("SELECT * FROM users")
    return render_template("users.html", rows=rows)

@app.route("/")
def portfolio():
    if "titles" not in session:
        session["titles"] = []
    return render_template("portfolio.html", titles=session["titles"])

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        title = request.form.get("title")
        session["titles"].append(title)
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        c.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)", 
                {'username':name, 'email':email, 'password':hashlib.sha256(str(password).encode("utf-8")).hexdigest()})
        conn.commit()
        return redirect("/users")


#@app.route("/goodbye")

if __name__ == "__main__":
    app.run()