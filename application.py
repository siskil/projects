from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    rows = db.execute("SELECT SUM(shares_number) summed, symbol FROM shares WHERE user_id = :id GROUP BY symbol",
                      id=session["user_id"])

    group = []
    for row in rows:
        if row["summed"] > 0:
            group_dict = {}
            quote = lookup(row["symbol"])
            group_dict["symbol"] = row["symbol"]
            group_dict["name"] = quote["symbol"]
            group_dict["share_number"] = row["summed"]
            group_dict["price"] = quote["price"]
            group_dict["total"] = quote["price"] * row["summed"]

            group.append(group_dict)

    ccash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
    for i in ccash:
        cash = i['cash']
    total_cash = 0
    for row in group:
        total_cash += row["total"]

    return render_template("/index.html", rows=group, cash=cash, total_cash=total_cash + cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        if not request.form.get("symbol") or lookup(request.form.get("symbol")) == None:
            return apology("provide valid symbol", 400)

        if not request.form.get("shares"):
            return apology("provide shares number", 400)

        shares = request.form.get("shares")
        if not shares.isdigit():
            return apology("provide valid number", 400)

        quote = lookup(request.form.get("symbol"))
        shares_number = int(request.form.get("shares"))
        price = quote["price"] * shares_number

        username = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        name = username[0]['username']

        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        if cash[0]['cash'] < price:
            return apology("not enough cash", 403)

        else:
            db.execute("INSERT INTO shares (user_id, shares_number, price, name, symbol, bought_sold) VALUES (:id, :shares_number, :price, :username, :symbol, :buy)",
                       id=session["user_id"], shares_number=shares_number, price=price, username=name, symbol=request.form.get("symbol"), buy="Bought")

            cash_left = cash[0]['cash'] - price

            db.execute("UPDATE users SET cash = :cash_left WHERE id = :id",
                       cash_left=cash_left, id=session["user_id"])

            return redirect("/")

    if request.method == "GET":
        return render_template("/buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM shares WHERE user_id = :id", id=session["user_id"])
    return render_template("/history.html", shares=rows)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    # POST
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        if quote == None:
            return apology("symbol doesn`t exist", 400)

        return render_template("quoted.html", name=quote["name"], symbol=request.form.get("symbol"), price=quote["price"])

    # GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":

        # username submitted?
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # password submitted?
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # password resubmitted to ensure corectness?
        elif not request.form.get("confirmation"):
            return apology("must retype password", 400)

        # passwords match?
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 400)

        rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                          username=request.form.get("username"), hash=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))

        # unique username?
        if not rows:
            return apology("username taken", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("provide valid symbol", 400)

        if not request.form.get("shares"):
            return apology("provide shares number", 400)

        shares = request.form.get("shares")
        if not shares.isdigit():
            return apology("provide valid number", 400)

        shares = db.execute("SELECT SUM(shares_number) FROM shares WHERE user_id = :user_id AND symbol = :symbol",
                            user_id=session["user_id"], symbol=request.form.get("symbol"))
        for i in shares:
            s_nr = i['SUM(shares_number)']
            if s_nr == None:
                return apology("you have no such symbol", 400)
            elif int(request.form.get("shares")) > s_nr:
                return apology("not enough shares", 400)
            else:
                s_left = s_nr - int(request.form.get("shares"))

                username = db.execute(
                    "SELECT username FROM users WHERE id = :id", id=session["user_id"])
                name = username[0]['username']

                quote = lookup(request.form.get("symbol"))
                price = quote["price"] * int(request.form.get("shares"))
                cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

                db.execute("INSERT INTO shares (user_id, shares_number, price, name, symbol, bought_sold) VALUES (:id, :shares_number, :price, :username, :symbol, :buy)",
                           id=session["user_id"], shares_number=-int(request.form.get("shares")), price=price, username=name, symbol=request.form.get("symbol"), buy="Sold")

                cash_new = cash[0]['cash'] + price

                db.execute("UPDATE users SET cash = :cash_new WHERE id = :id",
                           cash_new=cash_new, id=session["user_id"])

    elif request.method == "GET":

        symbols = db.execute("SELECT DISTINCT symbol FROM shares WHERE user_id = :id GROUP BY symbol HAVING SUM(shares_number) > 0",
                             id=session["user_id"])

        return render_template("sell.html", symbols=symbols)

    return redirect("/")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)