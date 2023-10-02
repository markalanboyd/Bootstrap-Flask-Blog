import os
import requests
import smtplib

import dotenv
from flask import Flask, render_template, request
from datetime import datetime

dotenv.load_dotenv()

EMAIL = os.getenv("EMAIL")
PW = os.getenv("PW")

app = Flask(__name__)

posts_url = "https://api.npoint.io/ba368df6b87dc2b49747"
response = requests.get(posts_url)
posts = response.json()


@app.context_processor
def inject_year():
    return {"year": datetime.now().year}


@app.route("/")
def home():
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


def parse_message(request):
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]

    email_content = f"""Contact submission form from {name}
    From: {email}
    Phone: {phone}
    Message: {message}
    """

    return email_content


def send_mail(from_email, from_pw, request):
    email_content = parse_message(request)
    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587
    smtp_object = smtplib.SMTP(smtp_server, smtp_port)
    smtp_object.starttls()
    smtp_object.login(from_email, from_pw)
    smtp_object.sendmail(from_email, from_email, email_content)
    smtp_object.quit()


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        send_mail(EMAIL, PW, request)
        return "Success!"
    return render_template("contact.html")


@app.route("/post/<int:id>")
def post(id):
    post = posts[id]
    return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
