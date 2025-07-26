import tkinter as tk
from tkinter import ttk, messagebox
from db import db_connect
import webbrowser
import os

def refresh_tree(tree, cursor):
    for row in tree.get_children():
        tree.delete(row)

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
    name_entry = tk.Entry(popup, width=30).pack()
    tk.Label(popup, text="Category:", bg="#f0f0f0").pack(pady=5)
    category_entry = tk.Entry(popup, width=30).pack()
    tk.Label(popup, text="Price:", bg="#f0f0f0").pack(pady=5)
    price_entry = tk.Entry(popup, width=30).pack()
    tk.Label(popup, text="stock:", bg="#f0f0f0").pack(pady=5)
    stock_entry = tk.Entry(popup, width=30).pack()

    tk.Button(popup, text="Save", command=save, bg="#236A3A", fg="white").pack(pady=10)

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
            cursor.execute("UPDATE inventory SET price = %s, stock = %s WHERE id = %s",(new_price, new_qty, prod_id))
            db.commit()
            refresh_tree(tree, cursor)
            update_win.destroy()

    tk.Button(update_win, text="Update", command=save_update, bg="#236A3A", fg="white").pack(pady=10)

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
        from auth import show_login
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

        tk.Button(btn_frame, text="Add Product", bg="lightgray", fg="black",
                  command=lambda: add_product(cursor, tree)).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Update Product", bg="lightgray", fg="black",
                  command=lambda: update_product(tree, cursor, db)).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Delete Product", bg="lightgray", fg="black",
                  command=lambda: delete_product(tree, cursor, db)).pack(side="left", padx=10)

        tk.Button(btn_frame, text="View Customers", bg="lightgray", fg="black",
                  command=show_customers).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="View Sales History", bg="lightgray", fg="black",
          command=show_sales).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="View All Slips", bg="lightgray", fg="black",
          command=view_all_slips).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Logout", bg="lightgray", fg="black",
              command=lambda: show_login(root)).pack(side="left", padx=10)



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
        
    def show_sales():
        for widget in root.winfo_children():
            widget.destroy()

        root.title("Sales History")
        root.geometry("900x500")
        root.configure(bg="#f9f9f9")

        tk.Label(root, text="Sales History", font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

        columns = ("Username", "Items", "Total", "Date/Time")
        tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        tree.pack(padx=20, pady=10, fill="both", expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=200)

        cursor.execute("SELECT username, items, total, date_time FROM sales ORDER BY date_time DESC")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

        tk.Button(root, text="Back to Inventory", command=show_inventory,bg="gray", fg="white").pack(pady=10)

    def view_all_slips():
        for widget in root.winfo_children():
            widget.destroy()

        slips_folder = "slips"

        tk.Label(root, text="Saved Receipts", font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

        if not os.path.exists(slips_folder):
            tk.Label(root, text="No slips folder found.", font=("Arial", 12), bg="#f9f9f9").pack()
            return

        slips = [f for f in os.listdir(slips_folder) if f.endswith(".pdf")]
        if not slips:
            tk.Label(root, text="No receipts found in slips folder.", font=("Arial", 12), bg="#f9f9f9").pack()
            return

        listbox = tk.Listbox(root, font=("Courier", 10), width=70, height=20)
        listbox.pack(padx=20, pady=10, fill="both", expand=True)

        for slip in sorted(slips, reverse=True):
            listbox.insert("end", slip)

        def open_selected():
            selected = listbox.curselection()
            if selected:
                filename = listbox.get(selected[0])
                filepath = os.path.join(slips_folder, filename)
                webbrowser.open_new(rf"{filepath}")

        tk.Button(root, text="Open Selected", command=open_selected,
              bg="green", fg="white").pack(pady=5)

        tk.Button(root, text="Back to Inventory", command=show_inventory,
              bg="gray", fg="white").pack(pady=5)

    # Initial view
    show_inventory()

