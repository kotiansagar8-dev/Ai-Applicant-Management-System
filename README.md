# AI Applicant Management System

A Flask-based AI-powered Applicant Management System integrated with Machine Learning resume classification and candidate workflow tracking.

The system automates resume classification, candidate management, interview scheduling workflows, and recruitment tracking through a centralized HR dashboard.

---

# Features

* AI-powered resume classification
* Email-based resume downloading and processing
* HR dashboard for applicant management
* Candidate workflow management system
* Interview scheduling and tracking
* Resume PDF storage system
* Authentication system for admin login
* Candidate status management pipeline
* Organized resume processing architecture

---

# Candidate Workflow

The system follows a centralized candidate workflow pipeline:

```text
Resume Downloading
        ↓
AI Resume Classification
        ↓
Valid Resumes Stored
        ↓
HR Candidate Review
        ↓
Candidate Added to Dashboard
        ↓
SAVED
        ↓
INTERVIEW_SCHEDULED
        ↓
ON_HOLD / SELECTED / REJECTED
```

---

# System Architecture

## Architecture Overview

The project consists of two major modules:

### 1. Resume Classification Module

Responsible for:

* Downloading resumes from email
* Processing PDF resumes
* AI-based resume classification
* Storing classified resumes

### 2. Applicant Management Module

Responsible for:

* Candidate management dashboard
* Interview workflow handling
* Applicant status tracking
* Resume management
* HR operations

---

# Project Structure

```text
AI-Applicant-Management-System/
│
├── Classifier/
│   ├── email_classifier.py
│   ├── resume_model.pkl
│   ├── resume_vectorizer.pkl
│
├── flask_app/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   ├── services/
│   ├── database/
│   └── utils/
│
├── database_setup.sql
├── requirements.txt
├── .env.example
├── run.py
└── README.md
```

---

# Tech Stack

## Backend

* Flask
* Python

## Database

* MySQL

## Machine Learning

* Scikit-learn
* NumPy
* Pandas

## Frontend

* HTML
* CSS
* Jinja2 Templates

---

# Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/kotiansagar8-dev/Ai-Applicant-Management-System.git

cd Ai-Applicant-Management-System
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Important Dependency Compatibility

This project uses serialized Machine Learning models (`.pkl` files).

For proper model loading and consistent predictions, the following versions are REQUIRED:

```text
scikit-learn==1.4.2
numpy==1.26.4
```

Using different versions may cause:

* model loading errors
* vectorizer incompatibility
* inconsistent predictions
* pickle deserialization issues

---

# Environment Variables Setup

Create a `.env` file in the root directory.

Copy contents from `.env.example` and replace placeholder values with your own credentials.

Example:

```env
SECRET_KEY=your_secret_key

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=resume_management

EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

---

# Creating the `.env` File

## Step 1

In the root directory of the project, create a file named:

```text
.env
```

---

## Step 2

Copy the contents from:

```text
.env.example
```

into your newly created `.env` file.

---

## Step 3

Replace the placeholder values with your own credentials.

Example:

```env
SECRET_KEY=your_secret_key

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=resume_management

EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

---

# Gmail App Password Setup

This project uses Gmail IMAP access for downloading resumes from email.

Google no longer allows direct Gmail password usage for less secure apps.

You MUST generate a Gmail App Password.

---

## Step 1 — Enable 2-Step Verification

Go to:

```text
Google Account → Security → 2-Step Verification
```

Enable 2-Step Verification for your Gmail account.

---

## Step 2 — Generate App Password

After enabling 2-Step Verification:

Go to:

```text
Google Account → Security → App Passwords
```

---

## Step 3 — Create App Password

1. Select:

   * App: Mail
   * Device: Windows Computer (or Custom Name)

2. Click:

   ```text
   Generate
   ```

Google will generate a 16-character password.

Example:

```text
abcd efgh ijkl mnop
```

---

## Step 4 — Add App Password to `.env`

Use the generated password inside:

```env
EMAIL_PASSWORD=your_generated_app_password
```

Do NOT use your actual Gmail account password.

---

# Important Notes

* Never upload your `.env` file to GitHub
* Never expose your Gmail credentials publicly
* `.env` is already ignored using `.gitignore`

---

# Database Setup

## Step 1

Open MySQL.

---

## Step 2

Run:

```sql
SOURCE database_setup.sql;
```

This creates:

* users table
* candidates table
* sample admin account

---

# Running the Project

Start the Flask server:

```bash
python run.py
```

---

# Demo Credentials

```text
Username: admin
Password: admin123
```

---

# Screenshots & Demo

## Dashboard

(Add screenshot here)

## Candidate Workflow

(Add screenshot here)

## AI Resume Classification

(Add screenshot here)

## LinkedIn Demo Video

(Will be added soon)

---

# Future Improvements

* Automatic candidate information extraction from resumes
* Resume ranking system
* Email notifications for interview scheduling
* JWT-based authentication
* Role-based access control
* Docker deployment
* Cloud storage integration
* Analytics dashboard
* AI-based candidate matching

---

# Security Notes

* `.env` files are excluded from Git tracking
* Uploaded resumes are ignored using `.gitignore`
* Sensitive credentials are not stored in the repository

---

# Author

Sagar Kotian

Final Year B.Tech Student
Specialization: Robotics & Artificial Intelligence

---

# License

This project is intended for educational and portfolio purposes.
