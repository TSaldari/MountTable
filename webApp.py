''' Run commands:
set FLASK_APP=webApp.py
set FLASK_ENV=development
python -m flask run
'''
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, session
from argon2 import PasswordHasher
from functools import wraps

app = Flask(__name__)
app.secret_key = "asdfasdf" 

ph = PasswordHasher()

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # change if your MySQL user is different
        password="Comet1386!",  # your MySQL root/user password
        database="FoodManagementDB"
    )

def login_required(role=None):
    """
    Protect routes so that only logged-in users can access them.
    Optional 'role' parameter restricts access to a specific role.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for("login"))
            
            if role and session.get("role") != role:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("login"))
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["studentId"]  # from your form
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Logins WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            try:
                # Verify password with Argon2
                ph.verify(user["password_hash"], password)
                session["user_id"] = user["user_id"]
                session["role"] = user["role"]
                flash("Login successful!", "success")
                # Redirect based on role
                if user["role"] == "admin":
                    return redirect(url_for("adminDash")) 
                else:
                    return redirect(url_for("order_form"))  
            except:
                flash("Invalid password!", "danger")
        else:
            flash("User not found!", "danger")

    return render_template("login.html")

@app.route("/orderForm")
@login_required(role="student")
def order_form():
    return render_template("student/orderForm.html")

@app.route("/adminDash")
@login_required(role="admin")
def adminDash():
    return render_template("admin/adminDash.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required(role="student")
def student_dashboard():
    return render_template("students/dashboard.html")

@app.route("/dietary-preferences")
@login_required(role="student")
def dietary_preferences():
    return render_template("students/dietary-preferences.html")

@app.route("/orderHistory")
@login_required(role="student")
def order_history():
    return render_template("students/orderHistory.html")

@app.route("/account-settings")
@login_required(role="student")
def account_settings():
    return render_template("students/account-settings.html")
