-- Creates a database
CREATE DATABASE IF NOT EXISTS FoodManagementDB;
USE FoodManagementDB;

-- Table for logins (users)
CREATE TABLE Logins (
    user_id VARCHAR(15) PRIMARY KEY,   -- stores MT-########
    password_hash VARCHAR(255) NOT NULL, -- Argon2 or Bcrypt for hashes
    role ENUM('admin', 'staff', 'student', 'newUser') DEFAULT 'newUser',
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alergens reference table
CREATE TABLE Allergens (
    allergen_id INT AUTO_INCREMENT PRIMARY KEY,
    allergen_name VARCHAR(50) UNIQUE NOT NULL
);

-- User-Allergen join table
CREATE TABLE UserAllergens (
    user_id VARCHAR(15) NOT NULL,
    allergen_id INT NOT NULL,
    PRIMARY KEY (user_id, allergen_id),
    FOREIGN KEY (user_id) REFERENCES Logins(user_id),
    FOREIGN KEY (allergen_id) REFERENCES Allergens(allergen_id)
);

-- Table for food inventory
CREATE TABLE FoodInventory (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    quantity INT DEFAULT 0,
    weight VARCHAR(20), -- "lbs"
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for request forms
CREATE TABLE requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'approved', 'denied') DEFAULT 'pending'
);

-- Table for individual items
CREATE TABLE request_items (
    request_id INT NOT NULL,
    item_id INT NOT NULL,
    PRIMARY KEY (request_id, item_id),
    FOREIGN KEY (request_id) REFERENCES requests(request_id),
    FOREIGN KEY (item_id) REFERENCES FoodInventory(item_id)
);