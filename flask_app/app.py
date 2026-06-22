import os
from flask import Flask
from flask_app.routes.auth_routes import auth
from flask_app.routes.dashboard_routes import dashboard
from flask_app.routes.candidate_routes import candidate
from flask import send_from_directory, abort
app = Flask(__name__)
app.secret_key = "resume_system_secret"

app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(candidate)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RESUME_FOLDER = os.path.join(BASE_DIR, "..", "Uploads", "resumes")
ARCHIVE_FOLDER = os.path.join(BASE_DIR, "..", "Uploads", "archived_resumes")

@app.route("/resumes/<filename>")
def uploaded_file(filename):

    file_path_resume = os.path.join(RESUME_FOLDER, filename)
    file_path_archive = os.path.join(ARCHIVE_FOLDER, filename)

    if os.path.exists(file_path_resume):
        return send_from_directory(RESUME_FOLDER, filename)

    elif os.path.exists(file_path_archive):
        return send_from_directory(ARCHIVE_FOLDER, filename)

    else:
        abort(404)
@app.after_request
def add_header(response):

    response.cache_control.no_store = True
    return response
