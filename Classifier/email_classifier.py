
import os
import imaplib
import email
import hashlib
import pickle
from dotenv import load_dotenv

from pdfminer.high_level import extract_text as extract_pdf
from docx import Document

import warnings
warnings.filterwarnings("ignore")

import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)

import shutil
import re

# ================================
# LOAD ENV VARIABLES
# ================================
load_dotenv()

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

# ================================
# BASE PROJECT PATH
# ================================

BASE_DIR = r"C:\Users\user\Desktop\Resume_Management_System"

CLASSIFIER_DIR = os.path.join(BASE_DIR, "Classifier")
UPLOADS_DIR = os.path.join(BASE_DIR, "Uploads")

DOWNLOAD_FOLDER = os.path.join(UPLOADS_DIR, "downloads")
RESUME_FOLDER = os.path.join(UPLOADS_DIR, "resumes")

HASH_FILE = os.path.join(CLASSIFIER_DIR, "downloaded_hashes.pkl")

MODEL_PATH = os.path.join(CLASSIFIER_DIR, "resume_model.pkl")
VECTORIZER_PATH = os.path.join(CLASSIFIER_DIR, "resume_vectorizer.pkl")

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)

# ================================
# EMAIL CONFIG
# ================================
IMAP_SERVER = 'imap.gmail.com'

# ================================
# LOAD MODEL
# ================================
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

# To check for Model and Vectorizer Path
# print("MODEL_PATH:", MODEL_PATH)
# print("VECTORIZER_PATH:", VECTORIZER_PATH)

# print("MODEL TYPE:", type(model))
# print("VECTORIZER TYPE:", type(vectorizer))

# print("MODEL:", model)



# ================================
# HASH FUNCTION
# ================================
def file_hash(content):
    return hashlib.md5(content).hexdigest()

# ================================
# TEXT CLEANING
# ================================
def clean_text(text):
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,!?()\s]', '', text)
    return text.lower().strip()

# ================================
# TEXT EXTRACTION
# ================================
def extract_text_from_file(path):

    if path.lower().endswith('.pdf'):
        return extract_pdf(path)

    elif path.lower().endswith('.docx'):
        doc = Document(path)
        return '\n'.join([para.text for para in doc.paragraphs])

    return ""

# ================================
# EMAIL DOWNLOAD + CLASSIFICATION
# ================================
def connect_and_process():

    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "rb") as f:
            hashes = pickle.load(f)
    else:
        hashes = set()

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    download_count = 0
    resume_count = 0
    non_resume_count = 0
    error_count = 0

    typ, data = mail.search(None, 'ALL')

    for num in data[0].split():

        typ, msg_data = mail.fetch(num, '(RFC822)')
        raw_email = msg_data[0][1]

        message = email.message_from_bytes(raw_email)

        for part in message.walk():

            if part.get_content_maintype() == 'multipart':
                continue

            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()

            if filename and filename.lower().endswith(('.pdf', '.docx')):

                content = part.get_payload(decode=True)
                h = file_hash(content)

                content = part.get_payload(decode=True)
                h = file_hash(content)

                file_path = os.path.join(DOWNLOAD_FOLDER, filename)

                # ================================
                # DUPLICATE CHECK
                # ================================
                if h in hashes:
                    continue

                try:

                    # SAVE FILE
                    with open(file_path, 'wb') as f:
                        f.write(content)

                    hashes.add(h)
                    download_count += 1

                    # ================================
                    # CLASSIFY IMMEDIATELY
                    # ================================
                    text = extract_text_from_file(file_path).strip()

                    if not text:
                        continue

                    cleaned = clean_text(text)

                    vec = vectorizer.transform([cleaned])

                    prediction = model.predict(vec)[0]
                    
                    # ================================
                    # STORE RESULT
                    # ================================
                    if prediction == 1:

                        dest_path = os.path.join(
                            RESUME_FOLDER,
                            filename
                        )

                        shutil.move(file_path, dest_path)

                        resume_count += 1

                    else:
                        non_resume_count += 1

                except Exception as e:

                    error_count += 1

                    print(f"⚠️ Error processing '{filename}': {e}")

    # ================================
    # SAVE HASHES
    # ================================
    with open(HASH_FILE, "wb") as f:
        pickle.dump(hashes, f)

    # ================================
    # RETURN RESULTS FOR FLASK
    # ================================
    return {
        "processed_files": download_count,
        "resumes_found": resume_count,
        "non_resumes": non_resume_count,
        "errors": error_count
    }

# ================================
# FLASK ENTRY FUNCTION
# ================================
def run_classifier():
    return connect_and_process()

# ================================
# DIRECT RUN
# ================================
if __name__ == "__main__":

    result = run_classifier()

    print("\n✅ Processing complete")
    print(result)

