# Mount Table Web Application

A comprehensive web-based food management system designed for the Mount's free food resource: The Mount Table. This application enables students to request food items while allowing administrators to manage inventory, approve orders, and track food distribution analytics.

---

## 📋 Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation & Setup](#installation--setup)
- [User Guide](#user-guide)
  - [For Students](#for-students)
  - [For Administrators](#for-administrators)
- [Troubleshooting](#troubleshooting)
- [Security Features](#security-features)

---

## ✨ Features

### Student Features
- **User Registration**: Create an account with automatic ID generation
- **Food Ordering**: Browse and select food items from available inventory
- **Allergen Filtering**: Automatic filtering based on dietary restrictions
- **Order History**: View all past orders and their status
- **Order Tracking**: Receive updates and notes from administrators

### Administrator Features
- **Dashboard Analytics**: View statistics on food distribution, active users, and popular items
- **Order Management**: Approve, deny, or modify student food requests
- **Inventory Management**: Track stock levels and update quantities
- **User Management**: Approve new registrations and reset passwords
- **Low Stock Alerts**: Automatic notifications for items running low

---

## 💻 System Requirements

### Software Dependencies
- **Python**: Version 3.14 or higher
- **MySQL Server**: Version 8.0 or higher
- **MySQL Workbench**: For database management (required)
- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

### Python Packages
```
Flask==3.0.0
mysql-connector-python==8.2.0
argon2-cffi==23.1.0
python-dotenv==1.0.0
Flask-WTF==1.2.1
```

---

## 🚀 Installation & Setup

### Step 1: Install MySQL Server, MySQL Workbench, Visual Studio, and Python

1. Download and install **Python** from [python.org](https://www.python.org/downloads/)
1. Download and isntall **Visual Studio** from [microsoft.com](https://apps.microsoft.com/detail/xpdcfjdklzjlp8?hl=en-US&gl=US)
2. Download and install **MySQL Server** from [mysql.com](https://dev.mysql.com/downloads/mysql/)
3. Download and install **MySQL Workbench** from [mysql.com](https://dev.mysql.com/downloads/workbench/)
4. During MySQL Server installation, set a root password (you'll need this later, so remember it)

### Step 2: Set Up the Database Server

1. Open **MySQL Workbench**
2. Connect to your local MySQL server (default: `localhost:3306`)
3. Verify That login was possible, then move to the next steps.

### Step 3: Create/Populate the Database

1. Open a command prompt and traverse to the path of your MySQL Server's bin folder:
  ```bash
  cd "C:\Program Files\MySQL\MySQL Server 9.5\bin"
  ```
2. Login to your MySQL server, and enter your password:
  ```bash
  mysql -u root -p
  ```
3. Import the schema:
  ```bash
  CREATE DATABASE foodmanagementdb;
  USE foodmanagementdb;
  exit
  ```

4. Import the MountTable.sql dump file to get all your tables and information:
  ```bash
  mysql -u root -p foodmanagementdb < C:\Users\missy\Documents\MountTable\MountTable-main\instance\MountTable.sql
  ```

Congrats, your MySQL database should be all set up

### Step 4: Install Python Dependencies

1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to the project directory:
   ```bash
   cd "path/to/MountTable"
   ```
3. Install required packages:
   ```bash
   py -m pip install Flask mysql-connector-python argon2-cffi python-dotenv Flask-WTF
   ```

### Step 5: Configure Environment Variables

1. Look at the .env file in your project directory
2. Edit the following configuration in notepad(replace with your MySQL password):
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=YourMySQLPasswordHere
   DB_NAME=FoodManagementDB
   SECRET_KEY=your-secret-key-change-this-to-random-string
   ```

### Step 6: Run the Application

1. Set Flask environment variables:
   ```bash
   set FLASK_APP=webApp.py
   set FLASK_ENV=development
   ```

2. Start the Flask server:
   ```bash
   python -m flask run
   ```

3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

4. You should see the Mount Table home page!

---

## 📖 User Guide

### For Students

#### 1. Creating an Account

1. Click **"Sign Up"** on the home page
2. Fill out the registration form:
   - Enter your first and last name
   - Use your **Mount St. Mary's email** (@msmary.edu or @email.msmary.edu)
   - Create a secure password (minimum 8 characters)
   - Complete all required demographic information -- optional
3. Click **"Create Account"**
4. **Save your Mount Table ID** (format: MT-########) - you'll need this to log in!
5. Wait for administrator approval -- give it up to 24 hours!

#### 2. Logging In

1. Click **"Login"** on the home page
2. Enter your **Mount Table ID** (MT-########)
3. Enter your password
4. Click **"Log In"**

> **Forgot Your ID?** Click "Forgot ID" and visit Mount Table in person for assistance, or contact an administrator.

#### 3. Requesting Food

1. After logging in, click **"Request Food"** in the navigation menu
2. **Select Dietary Restrictions** (optional):
   - Check any allergens you need to avoid
   - Items containing those allergens will be automatically disabled
3. **Browse Food Categories**:
   - Soup, Broth, Ramen, Canned Meat/Fish
   - Cereal/Breakfast, Vegetables, Beans
   - Sauces, Snacks, Pasta, Rice/Potatoes, Drinks
4. **Select Items**:
   - Click the checkbox under items you want
   - Grayed-out items are either out of stock or contain your selected allergens
5. Click **"Submit Request"**
6. Review your order confirmation receipt

#### 4. Viewing Order History

1. Click **"Order History"** in the navigation menu
2. View all your past orders with:
   - Order number and date
   - Number of items requested
   - Status (Pending, Approved, or Denied)
3. Click **"View Details"** to see specific items and admin notes

#### 5. Order Status Meanings

- **Pending**: Your order is waiting for administrator review
- **Approved**: Your order is ready for pickup! Check for admin notes with pickup instructions
- **Denied**: Your order was not approved (check admin notes for reason)

#### 6. Picking Up Your Order

1. Check your order confirmation for admin notes
2. Visit Mount Table during operating hours
3. Bring your **Mount Table ID** or student ID
4. Staff will provide your approved items

---

### For Administrators

#### 1. Logging In

1. Navigate to the Mount Table home page
2. Click **"Login"**
3. Enter your admin **Mount Table ID**
4. Enter your admin password
5. You'll be redirected to the Admin Dashboard

#### 2. Dashboard Overview

The admin dashboard displays:
- **Active Users**: Number of students who have made requests
- **Pending Orders**: Orders awaiting your review
- **New Users**: Registrations awaiting approval
- **Food Statistics**: Average food per person, monthly distribution
- **Popular Items**: Most requested food items
- **Low Stock Alerts**: Items running low or out of stock

#### 3. Managing Orders

##### Viewing Order Details
1. From the dashboard, click **"Orders"** or scroll to "Pending Orders"
2. Click **"Details"** on any order to view:
   - Student information (name, ID, email)
   - Requested items with current stock levels
   - Order date and status

##### Approving Orders
1. Review the order details
2. Verify all items are in stock (shown in "Availability" column)
3. **Optional**: Add a note for the student (e.g., pickup instructions)
4. Click **"✓ Approve Order & Update Inventory"**
5. Inventory will be automatically reduced by 1 for each item

##### Denying Orders
1. Review the order details
2. **Recommended**: Add a note explaining why (e.g., "Out of stock items")
3. Click **"✗ Deny Order"**
4. Student will see the denial and your note

##### Modifying Orders
1. Open the order details page
2. Click **"Remove"** next to any item you want to remove
3. Confirm the removal
4. Then approve the modified order

##### Adding Notes to Orders
1. Open the order details page
2. Scroll to "Admin Note for Student"
3. Type your message (e.g., "Ready for pickup after 2pm")
4. Click **"Save Note"**
5. Students will see this note when viewing their order

#### 4. Managing Inventory

##### Viewing Inventory
1. Click **"Inventory"** in the navigation menu
2. View all food items with:
   - Current stock quantity
   - Category and weight
   - Stock status (Critical, Low, Moderate, Good)
   - Last updated date

##### Updating Stock Quantities
1. Find the item you want to update
2. Enter the adjustment amount in the input field (default: 1)
3. Click **"+"** to increase stock or **"−"** to decrease stock
4. Changes are saved immediately
5. You'll see a confirmation message

##### Stock Status Indicators
- **🔴 Critical**: Less than 15 units
- **🟡 Low**: 15-29 units
- **🟢 Moderate**: 30-49 units
- **✅ Good**: 50+ units

##### Best Practices
- Update inventory immediately after receiving shipments
- Perform weekly stock counts to ensure accuracy
- Monitor low stock alerts on the dashboard
- Order items before they reach critical levels

#### 5. Managing User Registrations

##### Approving New Users
1. From the dashboard, scroll to "New User Registrations"
2. Review user information:
   - Name and email
   - Mount Table ID
   - Registration date
3. Click **"Approve"** to grant access
4. User's role changes from "newUser" to "student"
5. Student can now log in and place orders

##### Denying Registrations
1. Review the registration
2. Click **"Deny"** to reject the registration
3. Confirm the action
4. User account will be deleted from the system

> **Note**: Always verify that users have valid Mount St. Mary's email addresses.

#### 6. User Lookup & Password Reset

##### Finding a User
1. Click **"User Lookup"** in the navigation menu
2. Enter the user's:
   - First name, OR
   - Last name, OR
   - Email address
3. Click **"Search Users"**
4. View search results with user details

##### Resetting Passwords
1. Find the user through User Lookup
2. Click **"Reset Password"** next to their name
3. **IMPORTANT**: Note their Mount Table ID to give to the student
4. Enter a new password (minimum 8 characters)
5. Confirm the password
6. Click **"Reset Password"**
7. **Provide the student with**:
   - Their Mount Table ID
   - Their new temporary password
8. Instruct them to log in and change their password

#### 7. Data Analytics

The dashboard provides key metrics:

- **Active Users**: Total students who have placed orders
- **Food Per Person**: Average pounds distributed per student
- **Monthly Distribution**: Total pounds distributed this month
- **Popular Items**: Top 5 most requested items
- **Orders Over Time**: Historical trends (last 6 months)

Use this data to:
- Plan inventory purchases
- Identify high-demand items
- Track program growth
- Report to stakeholders

#### 8. Admin Quick Actions

From the dashboard, you can quickly:
- **Update Inventory**: Jump to inventory management
- **Complete Registrations**: Approve pending users
- **Accept Orders**: Review and approve pending requests

---

## 🔒 Security Features

This application includes several security measures:

- **Password Hashing**: Argon2 encryption (industry standard) -- Also has auto password salting
- **CSRF Protection**: Prevents cross-site request forgery attacks
- **Role-Based Access**: Students and admins have separate permissions
- **Session Management**: Automatic timeout after inactivity
- **SQL Injection Prevention**: Parameterized queries throughout
- **Environment Variables**: Sensitive credentials stored securely

### Security Best Practices

**For Administrators:**
- Never share admin credentials
- Use strong, unique passwords
- Log out when finished
- Regularly update passwords
- Monitor user activity for suspicious behavior

**For Students:**
- Keep your Mount Table ID secure
- Don't share your password
- Log out on shared computers
- Report suspicious activity immediately

---

## 📄 License & Credits

**Developed by**: Thomas E. Saldari, Jr
**Institution**: Mount St. Mary's University  
**Year**: 2025  

This application is designed for educational and operational use by Mount St. Mary's University Mount Table free food resource program.

---

**Thank you for using Mount Table Food Management System!** 🍽️
