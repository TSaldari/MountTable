'''
Mount Table Web Application - Created solely by Thomas Saldari
============================================
A Flask-based web application for managing MSMU's free food resource system.
Allows students to request food items and administrators to manage inventory and approve orders.

Run commands:
set FLASK_APP=webApp.py
set FLASK_ENV=development
python -m flask run
'''

# ============== IMPORTS ==============
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, session
from argon2 import PasswordHasher
from functools import wraps
import random
import json
import os
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

# ============== APPLICATION SETUP ==============
# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'asdfasdf')  # Fallback for development

# Enable CSRF protection
csrf = CSRFProtect(app)

# Initialize password hasher (Argon2)
ph = PasswordHasher()

# ============== DATABASE CONNECTION ==============
def get_db_connection():
    """
    Create and return a MySQL database connection using environment variables.
    
    Returns:
        mysql.connector.connection: Database connection object
    """
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME', 'FoodManagementDB')
    )

# ============== AUTHENTICATION DECORATOR ==============
def login_required(role=None):
    """
    Decorator to protect routes and restrict access based on user role.
    
    Args:
        role (str, optional): Required role ('admin' or 'student'). If None, any authenticated user can access.
    
    Returns:
        function: Decorated function that checks authentication and authorization
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Check if user is logged in
            if "user_id" not in session:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for("login"))
            
            # Check if user has required role
            if role and session.get("role") != role:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("login"))
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

# ============== UTILITY FUNCTIONS ==============
def generate_user_id(cursor):
    """
    Generate a unique user ID in format MT-########.
    
    Args:
        cursor: MySQL cursor object to check for duplicates
    
    Returns:
        str: Unique user ID (e.g., 'MT-12345678')
    """
    while True:
        user_id = "MT-" + str(random.randint(10000000, 99999999))
        cursor.execute("SELECT 1 FROM Logins WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():  # No duplicate found
            return user_id

# ============== PUBLIC ROUTES ==============

@app.route("/")
def index():
    """
    Home page - displays welcome message and user information if logged in.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    student_id = session.get("user_id")
    
    # Get user details from database
    cursor.execute(
        "SELECT user_id, first_name, last_name FROM Logins WHERE user_id = %s",
        (student_id,)
    )
    user_info = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # Prepare user display information
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

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page - authenticates users and redirects based on role.
    GET: Display login form
    POST: Validate credentials and create session
    """
    # Redirect if already logged in
    if "user_id" in session:
        role = session.get("role")
        if role == "admin":
            return redirect(url_for("adminDash"))
        elif role == "student":
            return redirect(url_for("index"))

    # Process login form submission
    if request.method == "POST":
        user_id = request.form["studentId"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch user from database
        cursor.execute("SELECT * FROM Logins WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            try:
                # Verify password with Argon2
                ph.verify(user["password_hash"], password)
                
                # Create session
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

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration page - creates new user accounts with 'newUser' role (requires admin approval).
    GET: Display registration form
    POST: Validate and create new user account
    """
    # Redirect if already logged in
    if "user_id" in session:
        role = session.get("role")
        if role == "admin":
            return redirect(url_for("adminDash"))
        else:
            return redirect(url_for("index"))

    # Process registration form submission
    if request.method == "POST":
        password = request.form["password"]
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if email already exists
        cursor.execute("SELECT email FROM Logins WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            conn.close()
            flash("This email address is already registered. Please use a different email or visit the Mount Table if you forgot your password.", "danger")
            return render_template("register.html")

        # Hash password with Argon2
        password_hash = ph.hash(password)

        # Generate unique MT-######## ID
        user_id = generate_user_id(cursor)

        try:
            # Insert new user with 'newUser' role (requires admin approval)
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
            
        except mysql.connector.errors.IntegrityError as e:
            # Handle database integrity errors
            cursor.close()
            conn.close()
            
            if "Duplicate entry" in str(e) and "email" in str(e):
                flash("This email address is already registered. Please use a different email.", "danger")
            else:
                flash("Registration failed due to a database error. Please try again.", "danger")
            
            return render_template("register.html")

    return render_template("register.html")

@app.route("/logout")
def logout():
    """
    Logout - clears session and redirects to login page.
    """
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ============== STUDENT ROUTES ==============

@app.route("/orderForm", methods=["GET", "POST"])
@login_required(role="student")
def order_form():
    """
    Food request form - allows students to select food items and submit orders.
    GET: Display form with available items
    POST: Process order submission and create request in database
    """
    # Allergen mapping for food items
    ALLERGEN_MAP = {
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
        "Boxed Milk": [],
        
        # Canned Vegetables
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

    # Get user details
    cursor.execute(
        "SELECT user_id, first_name, last_name FROM Logins WHERE user_id = %s",
        (student_id,)
    )
    user_info = cursor.fetchone()
    
    # Prepare user display information
    if user_info:
        first_name = user_info.get('first_name') or ''
        last_name = user_info.get('last_name') or ''
        user_name = f"{first_name} {last_name}".strip() or "Student"
        display_id = user_info.get('user_id') or student_id 
    else:
        user_name = "Guest User"
        display_id = student_id

    # Get inventory data for availability checking
    cursor.execute("SELECT item_name, quantity FROM FoodInventory")
    inventory_results = cursor.fetchall()
    
    # Create inventory dictionary
    inventory_data = {
        item['item_name']: item['quantity'] 
        for item in inventory_results
    }
    
    conn.close()

    # Process order submission
    if request.method == "POST":
        selected_items = request.form.getlist("items")
        student_id = session.get("user_id")

        # Validate that items were selected
        if not selected_items:
            return render_template("student/orderForm.html", 
                                 inventory_data=json.dumps(inventory_data),
                                 user_name=user_name,
                                 user_id=display_id,
                                 allergen_data=json.dumps(ALLERGEN_MAP))
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Create new request
        cursor.execute("INSERT INTO requests (student_id) VALUES (%s)", (student_id,))
        request_id = cursor.lastrowid

        # Link selected items to request
        for item_name in selected_items:
            cursor.execute("SELECT item_id FROM FoodInventory WHERE item_name = %s", (item_name,))
            result = cursor.fetchone()
            if result:
                cursor.execute("INSERT INTO request_items (request_id, item_id) VALUES (%s, %s)",
                             (request_id, result["item_id"]))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("order_confirmation", request_id=request_id))

    # Display order form
    return render_template("student/orderForm.html", 
                         inventory_data=json.dumps(inventory_data),
                         user_name=user_name,
                         user_id=display_id,
                         allergen_data=json.dumps(ALLERGEN_MAP))

@app.route("/orderHistory")
@login_required(role="student")
def order_history():
    """
    Order history page - displays all orders for the logged-in student.
    Shows order status, date, and item count.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    student_id = session.get("user_id")
    
    # Get user details
    cursor.execute(
        "SELECT user_id, first_name, last_name FROM Logins WHERE user_id = %s",
        (student_id,)
    )
    user_info = cursor.fetchone()
    
    if user_info:
        first_name = user_info.get('first_name') or ''
        last_name = user_info.get('last_name') or ''
        user_name = f"{first_name} {last_name}".strip() or "Student"
        display_id = user_info.get('user_id') or student_id
    else:
        user_name = "Guest User"
        display_id = student_id
    
    # Get all orders for this student
    cursor.execute("""
        SELECT 
            r.request_id,
            r.request_date,
            r.status,
            COUNT(ri.item_id) as item_count
        FROM requests r
        LEFT JOIN request_items ri ON r.request_id = ri.request_id
        WHERE r.student_id = %s
        GROUP BY r.request_id, r.request_date, r.status
        ORDER BY r.request_date DESC
    """, (student_id,))
    
    orders = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template(
        "student/orderHistory.html",
        orders=orders,
        user_name=user_name,
        user_id=display_id
    )

@app.route("/order_confirmation/<int:request_id>")
@login_required(role="student")
def order_confirmation(request_id):
    """
    Order confirmation page - displays details of a specific order.
    Verifies order belongs to logged-in student.
    Shows order items, status, and admin notes if any.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    student_id = session.get("user_id")
    
    # Get order details (verify ownership)
    cursor.execute("""
        SELECT r.request_id, r.student_id, r.request_date, r.status, r.admin_note,
               l.first_name, l.last_name
        FROM requests r
        JOIN Logins l ON r.student_id = l.user_id
        WHERE r.request_id = %s AND r.student_id = %s
    """, (request_id, student_id))
    
    order = cursor.fetchone()
    
    if not order:
        cursor.close()
        conn.close()
        flash("Order not found.", "danger")
        return redirect(url_for("order_form"))
    
    # Get all items in order
    cursor.execute("""
        SELECT fi.item_name, fi.category, fi.weight
        FROM request_items ri
        JOIN FoodInventory fi ON ri.item_id = fi.item_id
        WHERE ri.request_id = %s
        ORDER BY fi.category, fi.item_name
    """, (request_id,))
    
    items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Prepare user name
    first_name = order.get('first_name') or ''
    last_name = order.get('last_name') or ''
    user_name = f"{first_name} {last_name}".strip() or "Student"
    
    return render_template(
        "student/orderConfirmation.html",
        order=order,
        items=items,
        user_name=user_name,
        user_id=student_id
    )

# ============== ADMIN ROUTES - DASHBOARD ==============

@app.route("/admin/adminDash")
@login_required(role="admin")
def adminDash():
    """
    Admin dashboard - displays overview of system statistics, pending orders, and new user registrations.
    Shows: active users, pending orders, inventory alerts, popular items, and new user registrations.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get count of active users (users who made at least one request)
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
    
    # Calculate average lbs of food per person
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
    monthly_distribution = round(result['monthly_lbs'] if result['monthly_lbs'] else 0, 1)
        
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
    
    # Get low stock items (quantity < 50)
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
    
    # Get inventory items for management preview
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

# ============== ADMIN ROUTES - ORDER MANAGEMENT ==============

@app.route("/admin/order_details/<int:request_id>")
@login_required(role="admin")
def order_details(request_id):
    """
    Order details page - displays full information about a specific order.
    Shows student info, order status, requested items, and stock availability.
    Allows admin to approve, deny, modify items, and add notes.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get order details
    cursor.execute("""
        SELECT r.request_id, r.student_id, r.request_date, r.status, r.admin_note,
               l.first_name, l.last_name, l.email
        FROM requests r
        JOIN Logins l ON r.student_id = l.user_id
        WHERE r.request_id = %s
    """, (request_id,))
    order = cursor.fetchone()
    
    # Get ordered items with current inventory status
    cursor.execute("""
        SELECT fi.item_id, fi.item_name, fi.category, fi.quantity, fi.weight
        FROM request_items ri
        JOIN FoodInventory fi ON ri.item_id = fi.item_id
        WHERE ri.request_id = %s
    """, (request_id,))
    items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("admin/order_details.html", order=order, items=items)

@app.route("/admin/approve_order/<int:request_id>", methods=["POST"])
@login_required(role="admin")
def approve_order(request_id):
    """
    Approve order - changes status to 'approved' and deducts items from inventory.
    Validates that all items are in stock before approving.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get all items in request
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
    
    # Deduct items from inventory
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
    """
    Deny order - changes status to 'denied' without affecting inventory.
    """
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

@app.route("/admin/remove_item/<int:request_id>/<int:item_id>", methods=["POST"])
@login_required(role="admin")
def remove_item(request_id, item_id):
    """
    Remove item from order - deletes a specific item from a pending order.
    Prevents removing the last item (admin should deny order instead).
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get item name for flash message
    cursor.execute("SELECT item_name FROM FoodInventory WHERE item_id = %s", (item_id,))
    item = cursor.fetchone()
    
    if not item:
        cursor.close()
        conn.close()
        flash("Item not found.", "danger")
        return redirect(url_for("order_details", request_id=request_id))
    
    # Check how many items are left in the order
    cursor.execute("""
        SELECT COUNT(*) as item_count 
        FROM request_items 
        WHERE request_id = %s
    """, (request_id,))
    
    result = cursor.fetchone()
    item_count = result['item_count']
    
    # Prevent removing the last item
    if item_count <= 1:
        cursor.close()
        conn.close()
        flash("Cannot remove the last item from an order. Please deny the entire order instead.", "warning")
        return redirect(url_for("order_details", request_id=request_id))
    
    # Remove the item from the request
    cursor.execute("""
        DELETE FROM request_items 
        WHERE request_id = %s AND item_id = %s
    """, (request_id, item_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f"'{item['item_name']}' has been removed from order #{request_id}.", "success")
    return redirect(url_for("order_details", request_id=request_id))

@app.route("/admin/update_note/<int:request_id>", methods=["POST"])
@login_required(role="admin")
def update_note(request_id):
    """
    Update admin note for order - adds or updates a note visible to the student.
    Used for pickup instructions, delays, or other order-specific messages.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    note = request.form.get("admin_note", "").strip()
    
    # Update the note (empty string will clear the note)
    cursor.execute(
        "UPDATE requests SET admin_note = %s WHERE request_id = %s",
        (note if note else None, request_id)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    if note:
        flash(f"Note updated for order #{request_id}.", "success")
    else:
        flash(f"Note cleared for order #{request_id}.", "info")
    
    return redirect(url_for("order_details", request_id=request_id))

# ============== ADMIN ROUTES - USER MANAGEMENT ==============

@app.route("/admin/approve_user/<user_id>", methods=["POST"])
@login_required(role="admin")
def approve_user(user_id):
    """
    Approve new user - changes role from 'newUser' to 'student', granting access to the system.
    """
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
    """
    Deny new user - deletes the user registration from the system.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete the user
    cursor.execute("DELETE FROM Logins WHERE user_id = %s", (user_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f"User {user_id} has been denied and removed.", "warning")
    return redirect(url_for("adminDash"))

@app.route("/admin/user_lookup", methods=["GET", "POST"])
@login_required(role="admin")
def user_lookup():
    """
    User lookup - search for users by name or email.
    Used for password resets and user account management.
    GET: Display search form
    POST: Search database and display results
    """
    if request.method == "POST":
        search_term = request.form.get("search_term", "").strip()
        
        if not search_term:
            flash("Please enter a name or email to search.", "warning")
            return render_template("admin/user_lookup.html", users=None)
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Search by first name, last name, email, or full name
        cursor.execute("""
            SELECT user_id, first_name, last_name, email, role, created_at
            FROM Logins
            WHERE first_name LIKE %s 
            OR last_name LIKE %s 
            OR email LIKE %s
            OR CONCAT(first_name, ' ', last_name) LIKE %s
            ORDER BY last_name, first_name
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not users:
            flash(f"No users found matching '{search_term}'.", "info")
        
        return render_template("admin/user_lookup.html", users=users, search_term=search_term)
    
    return render_template("admin/user_lookup.html", users=None)

@app.route("/admin/reset_password/<user_id>", methods=["GET", "POST"])
@login_required(role="admin")
def reset_password(user_id):
    """
    Reset user password - allows admin to set a new password for any user.
    GET: Display password reset form
    POST: Validate and update password
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get user details
    cursor.execute("""
        SELECT user_id, first_name, last_name, email, role
        FROM Logins
        WHERE user_id = %s
    """, (user_id,))
    
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        conn.close()
        flash("User not found.", "danger")
        return redirect(url_for("user_lookup"))
    
    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        
        # Validate passwords match
        if new_password != confirm_password:
            cursor.close()
            conn.close()
            flash("Passwords do not match. Please try again.", "danger")
            return render_template("admin/reset_password.html", user=user)
        
        # Validate password length
        if len(new_password) < 8:
            cursor.close()
            conn.close()
            flash("Password must be at least 8 characters long.", "danger")
            return render_template("admin/reset_password.html", user=user)
        
        # Hash the new password with Argon2
        password_hash = ph.hash(new_password)
        
        # Update the password in database
        cursor.execute(
            "UPDATE Logins SET password_hash = %s WHERE user_id = %s",
            (password_hash, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f"Password successfully reset for {user['first_name']} {user['last_name']} (ID: {user_id}).", "success")
        return redirect(url_for("user_lookup"))
    
    cursor.close()
    conn.close()
    
    return render_template("admin/reset_password.html", user=user)

# ============== ADMIN ROUTES - INVENTORY MANAGEMENT ==============

@app.route("/admin/inventory_management")
@login_required(role="admin")
def inventory_management():
    """
    Inventory management page - displays all food items with current stock levels.
    Allows admin to adjust quantities and monitor stock status.
    """
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
    """
    Update stock quantity - increases or decreases inventory for a specific item.
    
    Args:
        item_id: ID of the food item to update
        action: 'increase' or 'decrease'
    
    Validates that decrease operations don't result in negative stock.
    """
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