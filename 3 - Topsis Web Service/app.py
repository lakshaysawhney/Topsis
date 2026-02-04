import os
import re
import subprocess
import smtplib
from email.message import EmailMessage

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# CONFIGURATION

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")

if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise RuntimeError("Missing SENDER_EMAIL / SENDER_PASSWORD environment variables")

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

#  APP SETUP 

app = Flask(__name__)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# EMAIL FUNCTION

def send_email(receiver_email, attachment_path):
    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result File"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg.set_content("Please find attached the TOPSIS result file.")

    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="topsis_result.csv"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

# ROUTES 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    file = request.files.get("file")
    weights = request.form.get("weights")
    impacts = request.form.get("impacts")
    email = request.form.get("email")

    # BASIC VALIDATIONS

    if not file or not weights or not impacts or not email:
        return render_template("index.html", error="All fields are required")

    if not re.match(EMAIL_REGEX, email):
        return render_template("index.html", error="Invalid email format")

    weights_list = weights.split(",")
    impacts_list = impacts.split(",")

    if len(weights_list) != len(impacts_list):
        return render_template("index.html", error="Number of weights and impacts must be equal")

    if not all(i in ["+", "-"] for i in impacts_list):
        return render_template("index.html", error="Impacts must be + or - only")

    #  FILE HANDLING 

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, "result.csv")

    file.save(input_path)

    # CALL TOPSIS PACKAGE 

    try:
        subprocess.run(
            ["topsis", input_path, weights, impacts, output_path],
            check=True
        )
    except Exception:
        return render_template("index.html", error="Error while processing TOPSIS")

    # SEND EMAIL 

    try:
        send_email(email, output_path)
    except Exception:
        return render_template("index.html", error="Error while sending email")

    return render_template("index.html", success="Result sent to your email successfully")

#  MAIN 

if __name__ == "__main__":
    app.run(debug=True)