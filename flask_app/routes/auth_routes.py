from flask import Blueprint, session, request, redirect, render_template
from flask_app.database.db import get_db_connection

auth=Blueprint("auth",__name__)

@auth.route("/")
def load_login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM users
        WHERE username = %s
        AND password = %s
    """

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        session["user"] = user["username"]
        return redirect("/dashboard")

    return render_template(
        "login.html",
        error="Invalid username or password"
    )


