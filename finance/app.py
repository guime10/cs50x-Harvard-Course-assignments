import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    #get user info to generate his portfolio
    stocks = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id
        )
    user_cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", user_id
        )

    #generate total value of stocks
    total_cash_stocks = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total"] = stock["price"] * stock["shares"]
        total_cash_stocks = total_cash_stocks + stock["total"]

    total_cash = total_cash_stocks + user_cash[0]["cash"]
    #generate his home page with user portfolio
    return render_template("index.html", stocks=stocks, user_cash=user_cash[0], total_cash=total_cash)

    # I used table class found on https://getbootstrap.com/docs/4.0/content/tables/#contextual-classes to get a better design and visual

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        #get user, symbol and shares input
        symbol = request.form.get("symbol")
        price = lookup(symbol)
        shares = (request.form.get("shares"))
        user_id = session["user_id"]
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", user_id
            )[0]["cash"]

        #check for mistakes
        if not symbol:
            return apology("Must give symbol")
        if price is None:
            return apology("Symbol not found")
        try:
            shares = int(shares)
            if shares < 1:
                return apology("Share number not allowed")
        except ValueError:
            return apology("share must be a positive integer", 400)

        #calculate total value of transaction
        transaction_value = shares * price["price"]

        #update user cash info
        if user_cash < (transaction_value):
            return apology("Not enought money to complete the transaction")

        new_cash = user_cash - transaction_value

        #update user cash on tables
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",new_cash, user_id
            )

        #update transaction table with correct date and time
        date = datetime.datetime.now()
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)", user_id, symbol.upper(), shares, price["price"], date
            )

        #confirm the transaction for the user
        flash("Successfully bought!")
        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # get user from user session
    user_id = session["user_id"]
    #get user transaction list
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?", user_id
        )
    # send info to html
    return render_template("history.html", transactions = transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        #get user input
        quote = lookup(request.form.get("symbol"))

        #check for possible user errors
        if quote is None:
            return apology("Must give a valid symbol")

        #return user search
        return render_template("quoted.html", name = quote["name"], price = quote["price"], symbol = quote["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method =="GET":
        return render_template("register.html")

    else:
        #get user inputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        #check for possible user mistakes
        if not username:
            return apology("Must give a valid Username")
        if not password:
            return apology("Must give a valid Password")
        if not confirmation:
            return apology("Must give confirmation")
        if password != confirmation:
            return apology("Passwords does not match")

        #generate hash for users password
        hash = generate_password_hash(password)

        # check user info and if theres no duality save user info on SQL table
        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
                )
        except:
            return apology("Username already in use")

        #remind user session
        session["user_id"] = new_user
        return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":
        #get user session and all stock symbols that he have
        user_id =  session["user_id"]
        user_symbol = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id
        )
        #send to html the info
        return render_template("sell.html", symbols = [row["symbol"] for row in user_symbol])

    else:
        #get sybol and shares input
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        #check for mistakes
        if not symbol:
            return apology("Must give symbol")

        #set stock symbol as uppercase only
        stock = lookup(symbol.upper())

        if not stock:
            return apology("Symbol not found")

        if shares < 1:
            return apology("Share Not Allowed")

        #calculate total value of transaction
        transaction_value = shares * stock["price"]

        #update user cash and shares info
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        new_cash = user_cash + transaction_value

        user_shares = db.execute(
            "SELECT shares FROM transactions where user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol
        )
        new_shares = user_shares[0]["shares"]

        #check if user have enought shaers to do this transaction
        if shares > new_shares:
            return apology("You don't have enought shares to do this transaction!")

        #update user cash on tables
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",new_cash, user_id
            )

        #update transaction table with correct date and time
        date = datetime.datetime.now()
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)", user_id, stock["symbol"], (-1) * shares, stock["price"], date
            )

        #confirm the transaction for the user
        flash("Successfully sold!")
        return redirect("/")

@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Deposit money on user balance"""
    if request.method == "GET":
        return render_template("deposit.html")

    else:
        new_value = int(request.form.get("deposit_value"))

        if not new_value:
            return apology("Must add deposit value")

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        new_cash = user_cash + new_value

        #update user cash on tables
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",new_cash, user_id
            )

        return redirect("/")

#note: i spent 2+ weeks working on this, there's no better feeling than completing this assignment and getting to see everything working properly (at least i hope it is)
# i want to set one signature for this acomplishment:
#                   ,,,,
#             ,;) .';;;;',
# ;;,,_,-.-.,;;'_,|I\;;;/),,_
#  `';;/:|:);{ ;;;|| \;/ /;;;\__
#      L;/-';/ \;;\',/;\/;;;.') \
#      .:`''` - \;;'.__/;;;/  . _'-._
#    .'/   \     \;;;;;;/.'_7:.  '). \_
#  .''/     | '._ );}{;//.'    '-:  '.,L
#.'. /       \  ( |;;;/_/         \._./;\   _,
# . /        |\ ( /;;/_/             ';;;\,;;_,
#  /         )__(/;;/_/                (;;'''''
# /        _;:':;;;;:';-._             );
#/        /   \  `'`   --.'-._         \/
#       .'     '.  ,'         '-,
#      /    /   r--,..__       '.\
#    .'    '  .'        '--._     ]
#    (     :.(;>        _ .' '- ;/
#    |      /:;(    ,_.';(   __.'
#     '- -'"|;:/    (;;;;-'--'
#           |;/      ;;(
#           ''      /;;|
#                   \;;|
#                    \/