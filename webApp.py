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
    #Protect routes so that only logged-in users can access them by role
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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    student_id = session.get("user_id")
    
    cursor.execute(
        "SELECT user_id, first_name, last_name FROM Logins WHERE user_id = %s",
        (student_id,)
    )
    user_info = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user_info:
        first_name = user_info.get('first_name') or ''
        last_name = user_info.get('last_name') or ''
        user_name = f"{first_name} {last_name}".strip() or "Student"
        display_id = user_info.get('user_id') or student_id 
    else:
        user_name = "Guest User"
        display_id = student_id
    
    return render_template("index.html",
                         user_name=user_name,
                         user_id=display_id)

@app.route("/login", methods=["GET","POST"])
def login():
    # If user is already logged in, redirect them
    if "user_id" in session:
        role = session.get("role")
        if role == "admin":
            return redirect(url_for("adminDash"))
        elif role == "student":
            return redirect(url_for("index"))

    # Checking id/pass       
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

    # Getting food item selections here and placing into db
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

# REMOVED THE DUPLICATE adminDash FUNCTION THAT WAS HERE (lines 280-283)

def generate_user_id(cursor):
    while True:
        user_id = "MT-" + str(random.randint(10000000, 99999999))
        cursor.execute("SELECT 1 FROM Logins WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():  # no duplicate found
            return user_id

@app.route("/register", methods=["GET", "POST"])
def register():
    # If user is already logged in, redirect them
    if "user_id" in session:
        role = session.get("role")
        if role == "admin":
            return redirect(url_for("adminDash"))
        else:
            return redirect(url_for("index"))

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

@app.route("/admin/adminDash")
@login_required(role="admin")
def adminDash():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get count of active users (users who have made at least one request)
    cursor.execute("""
        SELECT COUNT(DISTINCT student_id) as active_users 
        FROM requests
    """)
    active_users = cursor.fetchone()['active_users']
    
    # Get count of pending orders
    cursor.execute("""
        SELECT COUNT(*) as pending_orders 
        FROM requests 
        WHERE status = 'pending'
    """)
    pending_orders = cursor.fetchone()['pending_orders']
    
    # Get count of new users awaiting approval
    cursor.execute("""
        SELECT COUNT(*) as new_users 
        FROM Logins 
        WHERE role = 'newUser'
    """)
    new_users = cursor.fetchone()['new_users']
    
    # Calculate lbs of food per person
    cursor.execute("""
        SELECT 
            COALESCE(SUM(CAST(REPLACE(fi.weight, 'oz', '') AS DECIMAL(10,2))) / 16.0, 0) as total_lbs,
            (SELECT COUNT(DISTINCT student_id) FROM requests WHERE status = 'approved') as unique_students
        FROM requests r
        JOIN request_items ri ON r.request_id = ri.request_id
        JOIN FoodInventory fi ON ri.item_id = fi.item_id
        WHERE fi.weight LIKE '%oz%' AND r.status = 'approved'
    """)
    result = cursor.fetchone()

    if result and result['unique_students'] and result['unique_students'] > 0:
        food_per_person = round(result['total_lbs'] / result['unique_students'], 1)
    else:
        food_per_person = 0
    # Calculate monthly distribution
    cursor.execute("""
        SELECT 
            COALESCE(SUM(CAST(REPLACE(fi.weight, 'oz', '') AS DECIMAL(10,2))) / 16.0, 0) as monthly_lbs
        FROM requests r
        JOIN request_items ri ON r.request_id = ri.request_id
        JOIN FoodInventory fi ON ri.item_id = fi.item_id
        WHERE fi.weight LIKE '%oz%' 
        AND r.status = 'approved'
        AND MONTH(r.request_date) = MONTH(CURRENT_DATE())
        AND YEAR(r.request_date) = YEAR(CURRENT_DATE())
    """)
    result = cursor.fetchone()
    monthly_distribution = round(result['monthly_lbs'] if result['monthly_lbs'] else 0, 1)  # 
        
    # Get most popular items (top 5)
    cursor.execute("""
        SELECT 
            fi.item_name,
            fi.category,
            COUNT(*) as order_count
        FROM request_items ri
        JOIN FoodInventory fi ON ri.item_id = fi.item_id
        GROUP BY fi.item_id, fi.item_name, fi.category
        ORDER BY order_count DESC
        LIMIT 5
    """)
    popular_items = cursor.fetchall()
    
    # Get low stock items (quantity < 30 as threshold)
    cursor.execute("""
        SELECT 
            item_name,
            quantity,
            weight,
            CASE 
                WHEN quantity < 15 THEN 'low'
                WHEN quantity < 30 THEN 'medium'
                ELSE 'good'
            END as stock_status
        FROM FoodInventory
        WHERE quantity < 50
        ORDER BY quantity ASC
        LIMIT 5
    """)
    low_stock_items = cursor.fetchall()
    
    # Get pending orders with details
    cursor.execute("""
        SELECT 
            r.request_id,
            r.student_id,
            r.request_date,
            r.status,
            COUNT(ri.item_id) as item_count
        FROM requests r
        LEFT JOIN request_items ri ON r.request_id = ri.request_id
        WHERE r.status = 'pending'
        GROUP BY r.request_id, r.student_id, r.request_date, r.status
        ORDER BY r.request_date DESC
        LIMIT 10
    """)
    pending_order_list = cursor.fetchall()
    
    # Get inventory items for management table
    cursor.execute("""
        SELECT 
            item_id,
            item_name,
            category,
            quantity,
            weight,
            last_updated
        FROM FoodInventory
        ORDER BY last_updated DESC
        LIMIT 10
    """)
    inventory_items = cursor.fetchall()
    
    # Get new user registrations awaiting approval
    cursor.execute("""
        SELECT 
            user_id,
            first_name,
            last_name,
            email,
            created_at,
            role
        FROM Logins
        WHERE role = 'newUser'
        ORDER BY created_at DESC
    """)
    new_user_list = cursor.fetchall()
    
    # Get orders over time data (last 6 months)
    cursor.execute("""
        SELECT 
            DATE_FORMAT(request_date, '%Y-%m') as month,
            COUNT(*) as order_count
        FROM requests
        WHERE request_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
        GROUP BY DATE_FORMAT(request_date, '%Y-%m')
        ORDER BY month ASC
    """)
    orders_over_time = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template(
        "admin/adminDash.html",
        active_users=active_users,
        pending_orders=pending_orders,
        new_users=new_users,
        food_per_person=food_per_person,
        monthly_distribution=monthly_distribution,
        popular_items=popular_items,
        low_stock_items=low_stock_items,
        pending_order_list=pending_order_list,
        inventory_items=inventory_items,
        new_user_list=new_user_list,
        orders_over_time=orders_over_time
    )

@app.route("/orderHistory")
@login_required(role="student")
def order_history():
    return render_template("students/orderHistory.html")


# ============== ORDER MANAGEMENT ROUTES ==============

@app.route("/admin/approve_order/<int:request_id>", methods=["POST"])
@login_required(role="admin")
def approve_order(request_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get all items in this request
    cursor.execute("""
        SELECT ri.item_id, fi.item_name, fi.quantity
        FROM request_items ri
        JOIN FoodInventory fi ON ri.item_id = fi.item_id
        WHERE ri.request_id = %s
    """, (request_id,))
    
    items = cursor.fetchall()
    
    # Check if all items are in stock
    out_of_stock = []
    for item in items:
        if item['quantity'] <= 0:
            out_of_stock.append(item['item_name'])
    
    if out_of_stock:
        cursor.close()
        conn.close()
        flash(f"Cannot approve order #{request_id}. Out of stock: {', '.join(out_of_stock)}", "danger")
        return redirect(url_for("order_details", request_id=request_id))
    
    # Update request status to approved
    cursor.execute(
        "UPDATE requests SET status = 'approved' WHERE request_id = %s",
        (request_id,)
    )
    
    # Deduct each item from inventory (decrease quantity by 1)
    items_deducted = []
    for item in items:
        cursor.execute(
            "UPDATE FoodInventory SET quantity = quantity - 1 WHERE item_id = %s",
            (item['item_id'],)
        )
        items_deducted.append(item['item_name'])
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f"Order #{request_id} has been approved and inventory updated. Items deducted: {', '.join(items_deducted)}", "success")
    return redirect(url_for("adminDash"))

@app.route("/admin/deny_order/<int:request_id>", methods=["POST"])
@login_required(role="admin")
def deny_order(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE requests SET status = 'denied' WHERE request_id = %s",
        (request_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f"Order #{request_id} has been denied.", "warning")
    return redirect(url_for("adminDash"))

@app.route("/admin/order_details/<int:request_id>")
@login_required(role="admin")
def order_details(request_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get order details
    cursor.execute("""
        SELECT r.*, l.first_name, l.last_name, l.email
        FROM requests r
        JOIN Logins l ON r.student_id = l.user_id
        WHERE r.request_id = %s
    """, (request_id,))
    order = cursor.fetchone()
    
    # Get ordered items
    cursor.execute("""
        SELECT fi.item_name, fi.category, fi.quantity, fi.weight
        FROM request_items ri
        JOIN FoodInventory fi ON ri.item_id = fi.item_id
        WHERE ri.request_id = %s
    """, (request_id,))
    items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("admin/order_details.html", order=order, items=items)

# ============== USER MANAGEMENT ROUTES ==============

@app.route("/admin/approve_user/<user_id>", methods=["POST"])
@login_required(role="admin")
def approve_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE Logins SET role = 'student' WHERE user_id = %s",
        (user_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f"User {user_id} has been approved as a student.", "success")
    return redirect(url_for("adminDash"))

@app.route("/admin/deny_user/<user_id>", methods=["POST"])
@login_required(role="admin")
def deny_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Option 1: Delete the user
    cursor.execute("DELETE FROM Logins WHERE user_id = %s", (user_id,))
    
    # Option 2: Keep user but mark as denied (uncomment if you prefer this)
    # cursor.execute("UPDATE Logins SET role = 'denied' WHERE user_id = %s", (user_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f"User {user_id} has been denied and removed.", "warning")
    return redirect(url_for("adminDash"))


# ============== INVENTORY MANAGEMENT ROUTES ==============

@app.route("/admin/inventory_management")
@login_required(role="admin")
def inventory_management():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get all inventory items, ordered by category and name
    cursor.execute("""
        SELECT 
            item_id,
            item_name,
            category,
            quantity,
            weight,
            last_updated
        FROM FoodInventory
        ORDER BY category ASC, item_name ASC
    """)
    inventory_items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template(
        "admin/inventory_management.html",
        inventory_items=inventory_items
    )

@app.route("/admin/update_stock/<int:item_id>/<action>", methods=["POST"])
@login_required(role="admin")
def update_stock(item_id, action):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get the amount from form data (default to 1 if not provided)
    amount = int(request.form.get('amount', 1))
    
    # Get current item info
    cursor.execute("SELECT item_name, quantity FROM FoodInventory WHERE item_id = %s", (item_id,))
    item = cursor.fetchone()
    
    if not item:
        cursor.close()
        conn.close()
        flash("Item not found.", "danger")
        return redirect(url_for("inventory_management"))
    
    # Update quantity based on action
    if action == "increase":
        cursor.execute(
            "UPDATE FoodInventory SET quantity = quantity + %s WHERE item_id = %s",
            (amount, item_id)
        )
        new_quantity = item['quantity'] + amount
        flash(f"Increased stock for '{item['item_name']}' by {amount} to {new_quantity}.", "success")
    elif action == "decrease":
        if item['quantity'] >= amount:
            cursor.execute(
                "UPDATE FoodInventory SET quantity = quantity - %s WHERE item_id = %s",
                (amount, item_id)
            )
            new_quantity = item['quantity'] - amount
            flash(f"Decreased stock for '{item['item_name']}' by {amount} to {new_quantity}.", "warning")
        else:
            cursor.close()
            conn.close()
            flash(f"Cannot decrease stock for '{item['item_name']}' by {amount} - current stock is only {item['quantity']}.", "danger")
            return redirect(url_for("inventory_management"))
    else:
        cursor.close()
        conn.close()
        flash("Invalid action.", "danger")
        return redirect(url_for("inventory_management"))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for("inventory_management"))