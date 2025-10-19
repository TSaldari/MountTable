''' Run commands so i dont forget:
set FLASK_APP=webApp.py
set FLASK_ENV=development
python -m flask run
'''
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, session
from argon2 import PasswordHasher
from functools import wraps
import random
import json

app = Flask(__name__)
app.secret_key = "asdfasdf" 

ph = PasswordHasher()

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="Comet1386!",  # MySQL root/user password
        database="FoodManagementDB"
    )

def login_required(role=None):
    '''
    Protect routes so that only logged-in users can access them.
    Optional 'role' parameter restricts access to a specific role.
    '''
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
        user_id = request.form["studentId"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Logins WHERE user_id = %s", (user_id,))

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
                flash("Invalid ID or password!", "danger")
        else:
            flash("Invalid ID or password!", "danger")

    return render_template("login.html")

@app.route("/orderForm", methods=["GET", "POST"])
@login_required(role="student")
def order_form():

    # Maps Items to possible allergens
    ALLERGEN_MAP = {
        # Item Name: [Allergen Keys matching checkbox values]
        
        # Soups
        "Chicken Soup": ["gluten"],
        "Tomato Soup": [],
        "Vegetable Soup": [],
        "Vegetarian Soup": [],
        "Beef Stew": ["gluten"],
        "Chili": [],
        "Cream": [], 
        
        # Broths
        "Chicken Broth": [],
        "Beef Broth": [],
        "Vegetable Broth": [],
        
        # Ramen
        "Chicken Ramen": ["gluten"],
        "Beef Ramen": ["gluten"],
        
        # Canned Meat/Fish
        "Chicken": [],
        "Tuna": ["seafood"],
        "Sardines": ["seafood"],
        "Spam": [],
        "Vienna": [],
        
        # Cereal/Breakfast
        "Cereal": ["gluten", "nuts"], 
        "Oatmeal": [], 
        "Pop Tarts": ["gluten"],
        "Nut Butter": ["peanuts", "nuts"], 
        "Jelly": [],
        "Apple Butter": [],
        
        # Canned Vegetables
        "Boxed Milk": [],
        "Green Beans": [],
        "Peas": [],
        "Corn": [],
        "Diced Tomatoes": [],
        "Carrots": [],
        "Greens": [],
        "Beets": [],
        "Black Olives": [],

        # Beans
        "Black Beans": [],
        "Kidney Beans": [],
        "White Beans": [],
        "Chickpeas": [],
        "Pinto Beans": [],
        "Refried Beans": [],
        "Baked Beans": [],
        
        # Sauces/Condiments
        "Ketchup": [],
        "Tomato Sauce": [],
        "Salsa": [],
        "Alfredo Sauce": ["gluten"],
        "Salad Dressing": [],

        # Other
        "Cran Sauce": [],
        "Pumpkin": [],
        
        # Snacks 
        "Granola Bars": ["gluten", "nuts"],
        "Crackers": ["gluten"],
        "Chips": [],
        "Pretzels": ["gluten"],
        "Microwave Popcorn": [],
        "Fruit Cups": [],
        "Applesauce": [],
        
        # Pasta
        "Dry Pasta": ["gluten"],
        "Canned Meat Pasta": ["gluten"],
        "Canned Veg Pasta": ["gluten"],
        "Macaroni & Cheese": ["gluten"],
        "Egg Noodles": ["gluten"],
        "Flavored Noodle Side": ["gluten"],
        
        # Rice/Potatoes
        "White Rice": [],
        "Brown Rice": [],
        "Flavored Rice Side": ["gluten"],
        "Canned Potatoes": [],
        "Instant Potatoes": [],
        "Quinoa": [],
        
        # Drinks
        "Ground Coffee": [],
        "Black Tea": [],
        "Herbal Tea": [],
        "Iced Tea": [],
        "Drink Sticks": [],
        "Fruit Juice": []
    }

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    student_id = session.get("user_id")

    # Getting User Details
    cursor.execute(
        "SELECT user_id, first_name, last_name FROM Logins WHERE user_id = %s",
        (student_id,)
    )
    user_info = cursor.fetchone()
    
    # Define variables to pass to the template
    if user_info:
        first_name = user_info.get('first_name') or ''
        last_name = user_info.get('last_name') or ''
        
        # Normalizes the username
        user_name = f"{first_name} {last_name}".strip() or "Student"
        
        # User ID number
        display_id = user_info.get('user_id') or student_id 
    else:
        # In case of error go to this default
        user_name = "Guest User"
        display_id = student_id

    # Get Inventory Data 
    # Query the database for all item names and their quantity
    cursor.execute("SELECT item_name, quantity FROM FoodInventory")
    inventory_results = cursor.fetchall()
    
    # Dictionary for items and their quantity
    inventory_data = {
        item['item_name']: item['quantity'] 
        for item in inventory_results
    }
    
    # Close connection after getting this data
    conn.close()


    if request.method == "POST":
        selected_items = request.form.getlist("items")  # all checked food items
        student_id = session.get("user_id")

        if not selected_items: # restart page if no items are selected
            return render_template("student/orderForm.html", inventory_data=json.dumps(inventory_data),user_name=user_name,user_id=display_id,allergen_data=json.dumps(ALLERGEN_MAP))
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Create a new request
        cursor.execute("INSERT INTO requests (student_id) VALUES (%s)",(student_id,))
        request_id = cursor.lastrowid  # get the auto-increment ID

        # Link selected items to the request
        for item_name in selected_items:
            cursor.execute("SELECT item_id FROM FoodInventory WHERE item_name = %s",(item_name,))
            result = cursor.fetchone()
            if result:
                cursor.execute("INSERT INTO request_items (request_id, item_id) VALUES (%s, %s)",(request_id, result["item_id"]))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("order_form"))  # redirect to GET view

    # Handle GET request
    return render_template("student/orderForm.html", inventory_data=json.dumps(inventory_data),user_name=user_name,user_id=display_id,allergen_data=json.dumps(ALLERGEN_MAP))

@app.route("/adminDash")
@login_required(role="admin")
def adminDash():
    return render_template("admin/adminDash.html")

def generate_user_id(cursor):
    while True:
        user_id = "MT-" + str(random.randint(10000000, 99999999))
        cursor.execute("SELECT 1 FROM Logins WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():  # no duplicate found
            return user_id

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Generate secure Argon2 hash
        password_hash = ph.hash(password)

        # Generate unique MT-######## ID
        user_id = generate_user_id(cursor)

        # Insert new user (default role = newUser)
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")

        cursor.execute(
            """
            INSERT INTO Logins (user_id, password_hash, role, first_name, last_name, email)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, password_hash, "newUser", first_name, last_name, email)
        )
        conn.commit()

        cursor.close()
        conn.close()

        flash(f"Registration successful! You can now log in with ID: {user_id}.", "success")
        return redirect(url_for("login"))

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
