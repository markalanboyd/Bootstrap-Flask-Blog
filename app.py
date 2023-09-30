import requests
from flask import Flask, render_template
from datetime import datetime

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


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:id>")
def post(id):
    post = posts[id]
    return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
