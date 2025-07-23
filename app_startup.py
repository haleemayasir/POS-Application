import tkinter as tk
from display import display_products, switch_category
from cart import update_cart, charge, remove_selected
from inventory import products

def start_pos_app():
    global root, product_frame, cart_list, total_label, discount_var, search_var

    root = tk.Tk()
    root.title("POS App with Categories")
    root.geometry("900x600")

    # --- Top Bar (Search + Categories) ---
    top_bar = tk.Frame(root)
    top_bar.pack(fill="x", padx=10, pady=10)

    search_frame = tk.Frame(top_bar)
    search_frame.pack(side="left")
    tk.Label(search_frame, text="Search: ").pack(side="left")
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side="left")
    search_entry.bind("<KeyRelease>", lambda e: display_products())

    category_frame = tk.Frame(top_bar)
    category_frame.pack(side="right", padx=200)
    for cat in products:
        tk.Button(category_frame, text=cat, command=lambda c=cat: switch_category(c)).pack(side="left", padx=5)

    # --- Product Display ---
    product_frame = tk.Frame(root)
    product_frame.pack(pady=10)

    # --- Cart Section ---
    cart_frame = tk.Frame(root)
    cart_frame.place(x=700, y=20)

    tk.Label(cart_frame, text="Cart", font=("Arial", 14, "bold")).pack()
    cart_list = tk.Listbox(cart_frame, width=30, height=20)
    cart_list.pack()

    total_label = tk.Label(cart_frame, text="Total: $0.00", font=("Arial", 12))
    total_label.pack(pady=5)

    discount_var = tk.BooleanVar()
    tk.Checkbutton(cart_frame, text="Apply 10% discount", variable=discount_var, command=update_cart).pack()

    tk.Button(cart_frame, text="Charge", bg="green", fg="white", width=20, command=charge).pack(pady=10)
    tk.Button(cart_frame, text="Remove Selected", bg="red", fg="white", width=20, command=remove_selected).pack(pady=5)

    cart_list.bind("<Double-Button-1>", lambda e: remove_selected())

    display_products()
