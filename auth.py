import tkinter as tk
from tkinter import messagebox
from db import db_connect
from admin import open_admin_panel
from app_startup import start_pos_app

db = db_connect()
cursor = db.cursor()

def show_register(parent_window):
    for widget in parent_window.winfo_children():
        widget.destroy()

    parent_window.title("Register")
    parent_window.geometry("400x550")
    parent_window.configure(bg="#f0f0f0")

    tk.Label(parent_window, text="Create New Account", font=("Arial", 14, "bold"),
             bg="#f0f0f0", fg="#333").pack(pady=20)

    # --- Helper for aligned fields ---
    def create_input(label_text):
        frame = tk.Frame(parent_window, bg="#f0f0f0")
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, font=("Arial", 10), bg="#f0f0f0", width=14, anchor="w").pack(side="left")
        entry = tk.Entry(frame, width=28)
        entry.pack(side="left", padx=10)
        return entry

    # --- Form Fields ---
    first_name_entry = create_input("First Name:")
    last_name_entry = create_input("Last Name:")
    contact_entry = create_input("Contact No:")
    email_entry = create_input("Email:")
    address_entry = create_input("Address:")
    user_entry = create_input("Username:")
    pass_entry = create_input("Password:")
    pass_entry.config(show="*")

    # --- Role Dropdown ---
    role_var = tk.StringVar()
    role_frame = tk.Frame(parent_window, bg="#f0f0f0")
    role_frame.pack(pady=5)
    tk.Label(role_frame, text="Role:", font=("Arial", 10), bg="#f0f0f0", width=10, anchor="w").pack(side="left")
    role_menu = tk.OptionMenu(role_frame, role_var, "admin", "customer")
    role_menu.config(width=26)
    role_menu.pack(side="left", padx=10)

    # --- Register Logic ---
    def register_user():
        username = user_entry.get()
        password = pass_entry.get()
        role = role_var.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        contact = contact_entry.get()
        address = address_entry.get()

        if not all([username, password, role, first_name, last_name, email, contact, address]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if role not in ['admin', 'customer']:
            messagebox.showerror("Error", "Please select a valid role.")
            return

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists.")
            return

        cursor.execute("""
            INSERT INTO users (username, password, role, first_name, last_name, email, contact, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, password, role, first_name, last_name, email, contact, address))
        db.commit()
        messagebox.showinfo("Success", "Registered successfully! Please login.")
        show_login(parent_window)

    # --- Buttons ---
    btn_frame = tk.Frame(parent_window, bg="#f0f0f0")
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="Register", command=register_user, width=12, bg="blue",
              fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Back to Login", command=lambda: show_login(parent_window), width=12,
              bg="gray", fg="white", font=("Arial", 10)).pack(side="left", padx=10)



def show_login(existing_window=None):
    if existing_window:
        login_window = existing_window
        for widget in login_window.winfo_children():
            widget.destroy()
    else:
        login_window = tk.Tk()

    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.configure(bg="#f0f0f0")

    def attempt_login():
        username = user_entry.get()
        password = pass_entry.get()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            role = result[8]

            # 🧽 Clear current window instead of destroying it
            for widget in login_window.winfo_children():
                widget.destroy()

            if role == "admin":
                open_admin_panel(login_window)  # You'll also need to pass this window to your admin panel
            else:
               start_pos_app(login_window, result[6])
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")



    tk.Label(login_window, text="Login to Your Account", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333").pack(pady=20)

    user_frame = tk.Frame(login_window, bg="#f0f0f0")
    user_frame.pack(pady=5)
    tk.Label(user_frame, text="Username:", font=("Arial", 10), bg="#f0f0f0").pack(side="left")
    user_entry = tk.Entry(user_frame, width=30)
    user_entry.pack(side="left", padx=10)

    pass_frame = tk.Frame(login_window, bg="#f0f0f0")
    pass_frame.pack(pady=5)
    tk.Label(pass_frame, text="Password:", font=("Arial", 10), bg="#f0f0f0").pack(side="left")
    pass_entry = tk.Entry(pass_frame, width=30, show="*")
    pass_entry.pack(side="left", padx=10)

    btn_frame = tk.Frame(login_window, bg="#f0f0f0")
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="Login", command=attempt_login, width=12, bg="green", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Register", command=lambda: show_register(login_window), width=12, bg="blue", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)

    login_window.mainloop()
