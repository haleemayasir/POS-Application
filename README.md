# Perfume Store Point-of-Sale (POS) System

A desktop-based Point-of-Sale (POS) application developed using **Python Tkinter** for managing perfume store operations. The system provides an intuitive interface for sales processing, inventory management, customer management, and transaction tracking.

## Overview

This application is designed to streamline daily retail operations in a perfume store. It supports secure user authentication, product management, sales transactions, customer record handling, and receipt generation through a role-based access system.

The system uses **MySQL** as its backend database to store and manage products, customers, and transaction records efficiently.

---

## Features

### 🔐 User Authentication

* Secure login system
* Role-based access control
* Separate access levels for Admin and Cashier

### 🛒 Point-of-Sale (POS)

* Browse products by category
* Add products to shopping cart
* Update item quantities
* Apply discounts
* Select payment methods (Cash/Card)
* Generate purchase receipts
* Calculate totals automatically

### 📦 Inventory Management (Admin)

* Add new products
* Edit product details
* Delete products
* Manage stock quantities
* Organize products by category

### 👥 Customer Management

* Store customer information
* View customer records
* Maintain purchase-related data

### 📊 Transaction Management

* Record sales transactions
* Store purchase history
* Generate receipts for completed orders

---

## 👤 User Roles

### Admin

Admins have full access to the system and can:

* Manage inventory
* Add, update, and remove products
* View customer information
* Access sales records
* Launch and operate the POS interface

### Cashier

Cashiers can:

* Log in to the system
* Browse available products
* Add items to cart
* Apply discounts
* Process customer payments
* Generate receipts

---

## 🛠️ Technologies Used

| Category              | Technologies                    |
| --------------------- | ------------------------------- |
| Programming Language  | Python                          |
| GUI Framework         | Tkinter                         |
| Database              | MySQL                           |
| Database Connectivity | MySQL Connector                 |
| Image Processing      | Pillow (PIL)                    |
| Data Visualization    | Matplotlib                      |
| Data Handling         | Pandas                          |
| Development Tools     | Visual Studio Code, Git, GitHub |

---

## 📂 Project Structure

```text
Perfume-POS-System/
│
├── login.py              # User authentication
├── pos.py                # Point-of-Sale interface
├── admin.py              # Admin dashboard
├── inventory.py          # Product management
├── customer.py           # Customer management
├── db.py                 # Database connection and queries
├── receipts/             # Generated receipts
├── images/               # Product and UI assets
└── README.md
```

---

## 🗄️ Database

The application uses a MySQL database to manage:

* Product information
* Inventory records
* Customer details
* Sales transactions
* Receipt data

---

## 🚀 Installation

### Prerequisites

* Python 3.x
* MySQL Server
* Required Python packages

### Install Dependencies

```bash
pip install mysql-connector-python pillow pandas matplotlib
```

### Configure Database

1. Create a MySQL database.
2. Import the required tables.
3. Update database credentials in `db.py`.

### Run the Application

```bash
python login.py
```

---

## 📸 Screenshots

Add screenshots of:

* Login Screen
* Admin Dashboard
* Product Display Interface
* Shopping Cart
* Checkout Process
* Generated Receipt

---


