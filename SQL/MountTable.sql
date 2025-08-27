-- Create a database
CREATE DATABASE IF NOT EXISTS FoodManagementDB;
USE FoodManagementDB;

-- Table for logins (users)
CREATE TABLE Logins (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff', 'student') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for food inventory
CREATE TABLE FoodInventory (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    quantity INT DEFAULT 0,
    unit VARCHAR(20), -- e.g. "kg", "packs", "cans"
    expiration_date DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for request forms
CREATE TABLE Requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity_requested INT NOT NULL,
    status ENUM('pending', 'approved', 'denied') DEFAULT 'pending',
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Logins(user_id),
    FOREIGN KEY (item_id) REFERENCES FoodInventory(item_id)
);