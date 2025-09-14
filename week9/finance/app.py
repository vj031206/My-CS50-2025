import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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

    # Get user cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Get portfolio rows for this user
    rows = db.execute("SELECT stock, quantity FROM portfolio WHERE user_id = ?", session["user_id"])

    portfolio = []
    total = cash

    for row in rows:
        quote = lookup(row["stock"])
        price = quote["price"]
        value = price * row["quantity"]

        portfolio.append({
            "stock": row["stock"],
            "quantity": row["quantity"],
            "price": usd(price),
            "value": usd(value)
        })

        total += value

    return render_template("index.html", cash=usd(cash), total=usd(total), portfolio=portfolio)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    db.execute("CREATE TABLE IF NOT EXISTS portfolio (purchase_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, stock TEXT NOT NULL, quantity INTEGER NOT NULL, price NUMERIC NOT NULL, value NUMERIC NOT NULL, UNIQUE(user_id, stock), FOREIGN KEY(user_id) REFERENCES users(id))")

    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)
        shares = request.form.get("shares")

        if not shares or not shares.isdigit():
            return apology("quantity not entered", 400)

        shares = int(shares)

        if shares <= 0:
            return apology("quantity must be positive integer")

        quote = lookup(symbol)
        if quote is None:
            return apology(f"{symbol} doesn't exist")

        price = float(quote["price"])
        value = price * shares

        # Get user's cash
        row = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = row[0]["cash"]

        if value > cash:
            return apology("you can't afford this stock")

        # Update portfolio
        row = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND stock = ?",
                         session["user_id"], symbol)
        if row:
            db.execute(
                "UPDATE portfolio SET quantity = quantity + ?, value = value + ? WHERE user_id = ? AND stock = ?",
                shares, value, session["user_id"], symbol
            )
        else:
            db.execute(
                "INSERT INTO portfolio (user_id, stock, quantity, price, value) VALUES (?, ?, ?, ?, ?)",
                session["user_id"], symbol, shares, price, value
            )

        # Deduct cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", value, session["user_id"])
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        type = "BUY"
        db.execute("INSERT INTO transactions (user_id, stock, quantity, price, value, type, balance) VALUES(?,?,?,?,?,?,?)",
                   session["user_id"], symbol, shares, price, value, type, cash)

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    db.execute("CREATE TABLE IF NOT EXISTS transactions (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, stock TEXT NOT NULL, quantity INTEGER NOT NULL, price NUMERIC NOT NULL, value NUMERIC NOT NULL, type TEXT NOT NULL, balance NUMERIC NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))")
    history = db.execute(
        "SELECT stock, quantity, price, value, type, balance, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        session["user_id"]
    )

    return render_template("history.html", history=history, usd=usd)


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
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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

    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        if quote is None:
            return apology(f"{symbol} doesn't exist", 400)

        return render_template("quote.html", name=quote["name"], price=usd(quote["price"]), symbol=quote["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # validations
        if not username:
            return apology("must provide username", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("username already taken", 400)

        if not password:
            return apology("must provide password", 400)

        if not confirmation:
            return apology("must confirm password", 400)

        if password != confirmation:
            return apology("passwords don't match", 400)

        # insert user
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # log them in
        session["user_id"] = db.execute(
            "SELECT id FROM users WHERE username = ?", username
        )[0]["id"]

        return redirect("/")

    # GET method
    return render_template("registration.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":
        # Get all stocks the user owns
        rows = db.execute("SELECT stock FROM portfolio WHERE user_id = ?", session["user_id"])
        portfolio = [row["stock"] for row in rows]  # list of stock symbols
        return render_template("sell.html", portfolio=portfolio)

    # POST method
    symbol = request.form.get("symbol")
    shares_str = request.form.get("shares")

    # Validate inputs
    if not symbol:
        return apology("must provide symbol", 400)
    if not shares_str or not shares_str.isdigit():
        return apology("quantity must be a positive integer", 400)

    shares = int(shares_str)
    if shares <= 0:
        return apology("quantity must be positive", 400)

    # Check user owns enough shares
    row = db.execute("SELECT quantity FROM portfolio WHERE user_id = ? AND stock = ?",
                     session["user_id"], symbol)
    if not row:
        return apology("you don't own this stock", 400)

    owned_quantity = row[0]["quantity"]
    if shares > owned_quantity:
        return apology("can't sell more than you own", 400)

    # Get current stock price
    quote = lookup(symbol)
    if quote is None:
        return apology(f"{symbol} doesn't exist", 400)

    price = float(quote["price"])
    value = price * shares

    # Update portfolio
    if shares == owned_quantity:
        db.execute("DELETE FROM portfolio WHERE user_id = ? AND stock = ?",
                   session["user_id"], symbol)
    else:
        db.execute(
            "UPDATE portfolio SET quantity = quantity - ?, value = value - ? WHERE user_id = ? AND stock = ?",
            shares, value, session["user_id"], symbol
        )

    # Update user's cash
    db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", value, session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Record transaction
    db.execute(
        "INSERT INTO transactions (user_id, stock, quantity, price, value, type, balance) VALUES (?, ?, ?, ?, ?, ?, ?)",
        session["user_id"], symbol, shares, price, value, "SELL", cash
    )

    # Redirect to homepage
    return redirect("/")


@app.route("/add_cash", methods=["POST"])
@login_required
def add_cash():
    """ Add cash """

    add = float(request.form.get("add_cash"))
    if add <= 0:
        return apology("enter valid amount", 403)
    db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", add, session["user_id"])

    balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    db.execute(
        "INSERT INTO transactions (user_id, stock, quantity, price, value, type, balance) VALUES (?, ?, ?, ?, ?, ?, ?)",
        session["user_id"], "CASH", 0, 0, add, "DEPOSIT", balance
    )

    return redirect("/")
