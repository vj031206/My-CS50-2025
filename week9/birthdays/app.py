import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # storing name and checking if valid
        name = request.form.get("name")
        if not name:
            return redirect("/")

        # storing day and checking if valid
        day = request.form.get("day")
        if not name:
            return redirect("/")
        try:
            day = int(day)
        except ValueError:
            return redirect("/")
        if day < 1 or day > 31:  # should be from 1-31
            return redirect("/")

        month = request.form.get("month")
        if not name:
            return redirect("/")
        try:
            month = int(month)
        except ValueError:
            return redirect("/")
        if month < 1 or month > 12:  # should be from 1 to 12
            return redirect("/")

        # TODO: Add the user's entry into the database

        db.execute("INSERT INTO birthdays (name, day, month) VALUES(?,?,?)", name, day, month)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", birthdays=birthdays)

# to delete rows


@app.route("/delete", methods=["POST"])
def delete():

    # stores id via post in order to modify the table
    id_str = request.form.get("id")
    if not id_str:
        return redirect("/")
    try:
        id_int = int(id_str)
    except ValueError:
        return redirect("/")

    db.execute("DELETE FROM birthdays WHERE id = ?", id_int)

    # returns to our home page
    return redirect("/")

# to edit rows


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        # stores id via get to only retrieve data which is safer
        id_str = request.args.get("id")
        if not id_str:
            return redirect("/")
        try:
            id_int = int(id_str)
        except ValueError:
            return redirect("/")

        rows = db.execute("SELECT * FROM birthdays WHERE id = ?", id_int)
        if not rows:
            return redirect("/")

        birthday = rows[0]
        birthdays = db.execute("SELECT * FROM birthdays ORDER BY name")
        return render_template("index.html", birthdays=birthdays, mode="edit", birthday_to_edit=birthday)

    # storing updated values and adding them to the updated row
    id_str = request.form.get("id")
    name = request.form.get("name", "").strip()
    try:
        day = int(request.form.get("day", ""))
        month = int(request.form.get("month", ""))
        id_int = int(id_str)
    except (ValueError, TypeError):
        return redirect("/")

    if not name or not (1 <= day <= 31) or not (1 <= month <= 12):
        return redirect("/")

    db.execute("UPDATE birthdays SET name = ?, day = ?, month = ? WHERE id = ?",
               name, day, month, id_int)

    # returns to homepage
    return redirect("/")
