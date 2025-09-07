from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/orderForm")
def order_form():
    return render_template("orderForm.html")

@app.route("/register")
def register():
    return render_template("register.html")