from flask import Blueprint, session, redirect, request, render_template
from flask_app.database.db import get_db_connection

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
def dashboard_home():
    if "user" not in session:
        return redirect("/")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get all counts in ONE query (best approach)
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM candidates
        GROUP BY status
    """)

    rows = cursor.fetchall()

    # default structure
    counts = {
        "SAVED": 0,
        "INTERVIEW_SCHEDULED": 0,
        "ON_HOLD": 0,
        "SELECTED": 0,
        "REJECTED": 0
    }

    for row in rows:
        counts[row["status"]] = row["count"]

    # total candidates
    total_candidates = sum(counts.values())

    cursor.close()
    db.close()

    return render_template(
        "dashboard.html",
        user=session["user"],

        total_candidates=total_candidates,
        saved_count=counts["SAVED"],
        scheduled_count=counts["INTERVIEW_SCHEDULED"],
        onhold_count=counts["ON_HOLD"],
        selected_count=counts["SELECTED"],
        rejected_count=counts["REJECTED"]
    )

    