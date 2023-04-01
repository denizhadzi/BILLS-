import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash
from staninvest import staninvest
from elektro import elektro
from plin import plin
from rtv import rtv
from telemach import telemach
from helpers import apology, login_required
from calculating_bill import sendmessage

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set

location = os.getcwd()
file_name = "token.json"
path=os.path.join(location, file_name)
isdir = os.path.isfile(os.path.join(location, file_name))
if isdir == 0:
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    text = []
    all = ["ELEKTRO", "PLIN", "RTV", "STANINVEST", "TELEMACH"]

    if request.method == "GET":
        db.execute("UPDATE together SET ELEKTRO = 0 WHERE ELEKTRO ISNULL ")
        db.execute("UPDATE together SET PLIN = 0 WHERE PLIN ISNULL ")
        db.execute("UPDATE together SET RTV = 0 WHERE RTV ISNULL ")
        db.execute("UPDATE together SET STANINVEST = 0 WHERE STANINVEST ISNULL ")
        db.execute("UPDATE together SET TELEMACH = 0 WHERE TELEMACH ISNULL ")
        table_data=["ELEKTRO", "PLIN", "RTV", "STANINVEST", "TELEMACH"]
        table=db.execute("SELECT * FROM together ORDER BY DATA DESC")

        return render_template("index.html", table=table, table_data=table_data)
    else:
        subject = request.form.get("data")
        sum = request.form.get("sum")

        tabela_za_subject = db.execute("SELECT * FROM together WHERE DATA = ?", subject)[0]
        for i in all:
            if tabela_za_subject[i] <= 0:
                return apology("NOT ALL 5 INVOICES HAVE BEEN RECIVED YET", 400)
        for i in all:
            text_inside = i + ":" + "" + str(tabela_za_subject[i]) + "\n"
            text.append(text_inside)
            content = "ZDRAVO\n\n" + "".join(text) + "SUM:"+ "" + sum + "\n\n" + "LP,\n" + "DENIZ HM\n"
        sendmessage(subject, content)
        return redirect('/')


@app.route("/staninvest", methods=["GET", "POST"])
@login_required
def staninvest1():

    if request.method == "POST":
        smetki_staninvest = staninvest()
        if smetki_staninvest != None:
            for i in smetki_staninvest:
                    date1 = i
                    price1 = smetki_staninvest[date1]
                    db.execute("INSERT OR IGNORE INTO staninvest (DATA, STANINVEST) VALUES(?, ?)", date1, price1)
                    db.execute("INSERT OR IGNORE INTO together (DATA) VALUES(?)", i)
                    db.execute("UPDATE together SET STANINVEST = ? WHERE DATA = ?", price1, date1)
            return redirect("staninvest")
        else:
            return apology("No new INVOICES", 400)

    else:
        staninvest_list = db.execute("SELECT * FROM staninvest ORDER BY DATA DESC")
        return render_template("staninvest.html", table=staninvest_list)


@app.route("/elektro", methods=["GET", "POST"])
@login_required
def elektro1():

    if request.method == "POST":
        smetki_elektro = elektro()
        if smetki_elektro != None:
            for i in smetki_elektro:
                    date1 = i
                    price1 = smetki_elektro[date1]
                    db.execute("INSERT OR IGNORE INTO elektro (DATA, ELEKTRO) VALUES(?, ?)", date1, price1)
                    db.execute("INSERT OR IGNORE INTO together (DATA) VALUES(?)", i)
                    db.execute("UPDATE together SET ELEKTRO = ? WHERE DATA = ?", price1, date1)
            return redirect("elektro")
        else:
            return apology("No new INVOICES", 400)
    else:
        elektro_list = db.execute("SELECT * FROM elektro ORDER BY DATA DESC")
        return render_template("elektro.html", table=elektro_list)


@app.route("/plin", methods=["GET", "POST"])
@login_required
def plin1():

    if request.method == "POST":
        smetki_plin = plin()
        if smetki_plin != None:
            for i in smetki_plin:
                    date1 = i
                    price1 = smetki_plin[date1]
                    db.execute("INSERT OR IGNORE INTO plin (DATA, PLIN) VALUES(?, ?)", date1, price1)
                    db.execute("INSERT OR IGNORE INTO together (DATA) VALUES(?)", i)
                    db.execute("UPDATE together SET PLIN = ? WHERE DATA = ?", price1, date1)
            return redirect("plin")
        else:
            return apology("No new INVOICES", 400)
    else:
        plin_list = db.execute("SELECT * FROM plin ORDER BY DATA DESC")
        return render_template("plin.html", table=plin_list)


@app.route("/rtv", methods=["GET", "POST"])
@login_required
def rtv1():

    if request.method == "POST":
        smetki_rtv = rtv()
        if smetki_rtv != None:
            for i in smetki_rtv:
                    date1 = i
                    price1 = smetki_rtv[date1]
                    db.execute("INSERT OR IGNORE INTO rtv (DATA, RTV) VALUES(?, ?)", date1, price1)
                    db.execute("INSERT OR IGNORE INTO together (DATA) VALUES(?)", i)
                    db.execute("UPDATE together SET RTV = ? WHERE DATA = ?", price1, date1)
            return redirect("rtv")
        else:
            return apology("No new INVOICES", 400)
    else:
        rtv_list = db.execute("SELECT * FROM rtv ORDER BY DATA DESC")
        return render_template("rtv.html", table=rtv_list)

@app.route("/telemach", methods=["GET", "POST"])
@login_required
def telemach1():

    if request.method == "POST":
        smetki_telemach = telemach()
        if smetki_telemach != None:
            for i in smetki_telemach:
                    date1 = i
                    price1 = smetki_telemach[date1]
                    db.execute("INSERT OR IGNORE INTO telemach (DATA, TELEMACH) VALUES(?, ?)", date1, price1)
                    db.execute("INSERT OR IGNORE INTO together (DATA) VALUES(?)", i)
                    db.execute("UPDATE together SET TELEMACH = ? WHERE DATA = ?", price1, date1)
            return redirect("telemach")
        else:
            return apology("No new INVOICES", 400)

    else:
        telemach_list = db.execute("SELECT * FROM telemach ORDER BY DATA DESC")
        return render_template("telemach.html", table=telemach_list)




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")





