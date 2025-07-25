import tkinter as tk
from tkinter import ttk, messagebox
from db import db_connect

def refresh_tree(tree, cursor):
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)

    # Re-fetch and insert data
    cursor.execute("SELECT id, name, category, price, stock FROM inventory")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def add_product(cursor, tree):
    def save():
        name = name_entry.get()
        category = category_entry.get()
        price = price_entry.get()
        stock = stock_entry.get()

        if not name or not category or not price or not stock:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor.execute("INSERT INTO inventory (name, category, price, stock) VALUES (%s, %s, %s, %s)",
                           (name, category, float(price), int(stock)))
            cursor.connection.commit()
            popup.destroy()
            refresh_tree(cursor, tree)
            messagebox.showinfo("Success", "Product added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    popup = tk.Toplevel()
    popup.title("Add New Product")
    popup.geometry("300x250")
    popup.configure(bg="#f0f0f0")

    tk.Label(popup, text="Name:", bg="#f0f0f0").pack(pady=5)
    name_entry = tk.Entry(popup, width=30)
    name_entry.pack()

    tk.Label(popup, text="Category:", bg="#f0f0f0").pack(pady=5)
    category_entry = tk.Entry(popup, width=30)
    category_entry.pack()

    tk.Label(popup, text="Price:", bg="#f0f0f0").pack(pady=5)
    price_entry = tk.Entry(popup, width=30)
    price_entry.pack()

    tk.Label(popup, text="stock:", bg="#f0f0f0").pack(pady=5)
    stock_entry = tk.Entry(popup, width=30)
    stock_entry.pack()

    tk.Button(popup, text="Save", command=save, bg="green", fg="white").pack(pady=10)

def update_product(tree, cursor, db):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")
    prod_id = values[0]

    update_win = tk.Toplevel()
    update_win.title("Update Product")
    update_win.geometry("300x250")

    tk.Label(update_win, text="New Price").pack(pady=5)
    price_entry = tk.Entry(update_win)
    price_entry.insert(0, values[3])
    price_entry.pack(pady=5)

    tk.Label(update_win, text="New Stock").pack(pady=5)
    qty_entry = tk.Entry(update_win)
    qty_entry.insert(0, values[4])
    qty_entry.pack(pady=5)

    def save_update():
        new_price = price_entry.get()
        new_qty = qty_entry.get()

        if new_price and new_qty:
            cursor.execute("UPDATE inventory SET price = %s, stock = %s WHERE id = %s",
                           (new_price, new_qty, prod_id))
            db.commit()
            refresh_tree(tree, cursor)
            update_win.destroy()

    tk.Button(update_win, text="Update", command=save_update, bg="green", fg="white").pack(pady=10)

def delete_product(tree, cursor, db):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")
    prod_id = values[0]

    cursor.execute("DELETE FROM inventory WHERE id = %s", (prod_id,))
    db.commit()
    refresh_tree(tree, cursor)

def open_admin_panel(root):
    db = db_connect()
    cursor = db.cursor()

    def show_inventory():
        for widget in root.winfo_children():
            widget.destroy()

        root.title("Admin Panel - Inventory")
        root.geometry("900x500")
        root.configure(bg="#f9f9f9")

        tk.Label(root, text="Inventory Management", font=("Arial", 16, "bold"),
                 bg="#f9f9f9", fg="#333").pack(pady=10)

        # --- Search Section ---
        search_frame = tk.Frame(root, bg="#f9f9f9")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search by Name:", bg="#f9f9f9").pack(side="left", padx=5)

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=30)
        search_entry.pack(side="left", padx=5)

        def search_inventory():
            query = search_var.get().lower()
            cursor.execute("SELECT id, name, category, price, stock FROM inventory")
            results = cursor.fetchall()

            tree.delete(*tree.get_children())

            for row in results:
                if query in row[1].lower():
                    tree.insert("", "end", values=row)

        tk.Button(search_frame, text="Search", command=search_inventory,
                  bg="gray", fg="white").pack(side="left", padx=5)
        tk.Button(search_frame, text="Reset",
                  command=lambda: (search_var.set(""), refresh_tree(tree, cursor)),
                  bg="lightgray").pack(side="left", padx=5)

        # --- Inventory Table ---
        columns = ("id", "name", "category", "price", "stock")
        tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        tree.pack(padx=20, pady=10, fill="both", expand=True)

        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=100, anchor="center")

        refresh_tree(tree, cursor)

        # --- Buttons ---
        btn_frame = tk.Frame(root, bg="#f9f9f9")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Product", bg="blue", fg="white",
                  command=lambda: add_product(cursor, tree)).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Update Product", bg="orange", fg="white",
                  command=lambda: update_product(tree, cursor, db)).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Delete Product", bg="red", fg="white",
                  command=lambda: delete_product(tree, cursor, db)).pack(side="left", padx=10)

        tk.Button(btn_frame, text="View Customers", bg="purple", fg="white",
                  command=show_customers).pack(side="left", padx=10)

    def show_customers():
        for widget in root.winfo_children():
            widget.destroy()

        root.title("Registered Customers")
        root.geometry("900x500")
        root.configure(bg="#f9f9f9")

        tk.Label(root, text="Customer List", font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

        columns = ("First Name", "Last Name", "Contact", "Email", "Address", "Username")
        tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        tree.pack(padx=20, pady=10, fill="both", expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        cursor.execute("SELECT first_name, last_name, contact, email, address, username FROM users WHERE role = 'customer'")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

        tk.Button(root, text="Back to Inventory", command=show_inventory,
                  bg="gray", fg="white").pack(pady=10)

    # Initial view
    show_inventory()

