
from flask import Blueprint, session, redirect, request, render_template, flash, url_for
from flask_app.database.db import get_db_connection
from Classifier.email_classifier import run_classifier

import os
import shutil


# =========================================================
# BLUEPRINT
# =========================================================
candidate = Blueprint("candidate", __name__)


# =========================================================
# PATH CONFIGURATION
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..")
)

RESUME_FOLDER = os.path.join(
    PROJECT_ROOT,
    "Uploads",
    "resumes"
)

ARCHIVE_FOLDER = os.path.join(
    PROJECT_ROOT,
    "Uploads",
    "archived_resumes"
)


# =========================================================
# ADD CANDIDATE PAGE
# =========================================================
@candidate.route("/candidates/add")
def add_candidate():

    if "user" not in session:
        return redirect("/")

    resumes = os.listdir(RESUME_FOLDER)
    resume_count = len(resumes)

    return render_template(
        "add_candidate.html",
        resumes=resumes,
        resume_count=resume_count
    )


# =========================================================
# SELECT RESUME
# =========================================================
@candidate.route("/candidates/add/<filename>")
def select_resume(filename):

    if "user" not in session:
        return redirect("/")

    resume_path = os.path.join(RESUME_FOLDER, filename)

    return render_template(
        "candidate_form.html",
        resume=filename
    )


# =========================================================
# SAVE CANDIDATE
# =========================================================
@candidate.route("/candidates/save", methods=["POST"])
def save_candidate():

    if "user" not in session:
        return redirect("/")

    data = request.form

    # Extract Resume Filename
    resume_file = os.path.basename(data["resume"])

    # File Paths
    old_path = os.path.join(RESUME_FOLDER, resume_file)
    new_path = os.path.join(ARCHIVE_FOLDER, resume_file)

    # Move Resume to Archive Folder
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)

    # Database Connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert Candidate
    cursor.execute("""
        INSERT INTO candidates (
            candidate_name,
            email,
            phone_number,
            education,
            experience,
            current_company,
            current_designation,
            current_location,
            resume_path,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["candidate_name"],
        data["email"],
        data["phone_number"],
        data["education"],
        data["experience"],
        data["current_company"],
        data["current_designation"],
        data["current_location"],
        resume_file,
        "SAVED"
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/candidates/add")

# -------------------- Run CLassifier---------------------

@candidate.route("/fetch-resumes", methods=["POST"])
def fetch_resumes():

    result = run_classifier()

    # flash(
    #     f"{result['resumes_found']} new resumes found!",
    #     "success"
    # )

    return redirect(url_for("candidate.add_candidate"))

# =========================================================
# VIEW SAVED CANDIDATES
# =========================================================
@candidate.route("/candidates")
def show_all_candidates():

    if "user" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM candidates
        WHERE status = "SAVED"
    """

    cursor.execute(query)

    candidates = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "saved_candidate.html",
        candidates=candidates
    )


# =========================================================
# VIEW SCHEDULED CANDIDATES
# =========================================================
# =========================================================
# VIEW SCHEDULED CANDIDATES
# =========================================================
@candidate.route("/scheduled")
def show_scheduled_candidates():

    if "user" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM candidates
        WHERE status = "INTERVIEW_SCHEDULED"
        ORDER BY interview_date ASC
    """

    cursor.execute(query)

    candidates = cursor.fetchall()

    cursor.close()
    conn.close()

    # =====================================================
    # GROUP CANDIDATES BY INTERVIEW DATE
    # =====================================================
    grouped_candidates = {}

    for candidate in candidates:

        interview_date = candidate["interview_date"]

        # Handle NULL Dates
        if interview_date is None:
            interview_date = "No Date Assigned"

        # Create Date Group
        if interview_date not in grouped_candidates:
            grouped_candidates[interview_date] = []

        # Add Candidate Under That Date
        grouped_candidates[interview_date].append(candidate)

    return render_template(
        "scheduled_interviews.html",
        grouped_candidates=grouped_candidates
    )
# =========================================================
# VIEW ON-HOLD CANDIDATES
# =========================================================
@candidate.route("/on-hold")
def show_held_candidates():

    if "user" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM candidates
        WHERE status = "ON_HOLD"
    """

    cursor.execute(query)

    candidates = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "on_hold.html",
        candidates=candidates
    )


# =========================================================
# VIEW SELECTED CANDIDATES
# =========================================================
@candidate.route("/selected")
def show_selected_candidates():

    if "user" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM candidates
        WHERE status = "SELECTED"
    """

    cursor.execute(query)

    candidates = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "selected.html",
        candidates=candidates
    )


# =========================================================
# VIEW REJECTED CANDIDATES
# =========================================================
@candidate.route("/rejected")
def show_rejected_candidates():

    if "user" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM candidates
        WHERE status = "REJECTED"
    """

    cursor.execute(query)

    candidates = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "rejected.html",
        candidates=candidates
    )


# =========================================================
# BULK UPDATE CANDIDATE STATUS
# =========================================================
@candidate.route("/bulk_update_status", methods=["POST"])
def bulk_update_status():

    if "user" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()

    redirect_page = request.form.get("redirect_to", "saved")

    try:

        for key, value in request.form.items():

            # Skip Redirect Field
            if key == "redirect_to":
                continue

            # Ignore Non-Status Fields
            if not key.startswith("status_"):
                continue

            # Extract Candidate ID
            candidate_id_str = key.replace("status_", "")

            if not candidate_id_str.isdigit():
                continue

            candidate_id = int(candidate_id_str)

            # Update Candidate Status
            # Interview Date
            # Get Interview Date
            interview_date = request.form.get(
                f"interview_date_{candidate_id}"
            )

            # Update Candidate Status + Interview Date
            cursor.execute("""
                UPDATE candidates
                SET
                    status = %s,
                    interview_date = %s
                WHERE candidate_id = %s
            """, (
                value,
                interview_date if interview_date else None,
                candidate_id
            ))

        conn.commit()

    finally:
        cursor.close()
        conn.close()

    # Redirect to Correct Page
    if redirect_page == "scheduled":
        return redirect("/scheduled")

    elif redirect_page == "saved":
        return redirect("/candidates")

    elif redirect_page == "onhold":
        return redirect("/on-hold")

    return redirect("/candidates")


# =========================================================
# LOGOUT
# =========================================================
@candidate.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")