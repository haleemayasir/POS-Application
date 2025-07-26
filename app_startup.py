import tkinter as tk
from display import display_products, switch_category
from cart import update_cart, charge, remove_selected, increase_quantity, decrease_quantity
from inventory import get_products

products = get_products()

def start_pos_app(root, username):
    from auth import show_login
    import cart
    cart.logged_in_user = username  # pass username to cart

    for widget in root.winfo_children():
        widget.destroy()
    root.title("POS App")
    root.geometry("1000x600")
    root.configure(bg="#FFFFFF")  # App background

    # --- Top Bar (Search + Categories) ---
    top_bar = tk.Frame(root, bg="#FFFFFF")
    top_bar.pack(fill="x", padx=50, pady=10)

    search_frame = tk.Frame(top_bar, bg="#FFFFFF")
    search_frame.pack(side="left")
    tk.Label(search_frame, text="Search: ", bg="#FFFFFF", fg="#111827", font=("Arial", 10)).pack(side="left")

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var,bg="#D6D6D6")
    search_entry.pack(side="left")

    # --- Product Display Frame ---
    product_frame = tk.Frame(root, width=800, bg="#FFFFFF")
    product_frame.pack(side="left", fill="both", expand=True)
    
    # Trigger search on typing
    search_entry.bind("<KeyRelease>", lambda e: display_products(product_frame, search_var))

    # --- Category Buttons ---
    category_frame = tk.Frame(top_bar, bg="#FFFFFF")
    category_frame.pack(side="right", padx=200)
    for cat in products:
        tk.Button(category_frame,text=cat,bg="#D1D5DB", fg="#111827",activebackground="#9CA3AF",
            relief="raised",command=lambda c=cat: switch_category(c, product_frame, search_var)).pack(side="left", padx=5)

    # --- Cart Section ---
    cart_frame = tk.Frame(root, width=220, bg="#F9FAFB", bd=2, relief="groove", padx=8, pady=8)
    cart_frame.pack(side="right", fill="y", padx=10, pady=10)

    tk.Label(cart_frame, text="🛒 Cart", font=("Arial", 14, "bold"), bg="#F9FAFB", fg="#111827").pack(pady=(0, 10))

    cart_list = tk.Listbox(cart_frame, width=30, height=15, bd=1, relief="sunken", highlightthickness=0, font=("Arial", 10))
    cart_list.pack(pady=(0, 10))

    total_label = tk.Label(cart_frame, text="Total: Rs 0", font=("Arial", 12, "bold"), bg="#F9FAFB", fg="#0B6648")
    total_label.pack(pady=(0, 10))

    discount_var = tk.BooleanVar()
    tk.Checkbutton(cart_frame, text="Apply 10% discount", variable=discount_var, command=update_cart,
                   bg="#F9FAFB", fg="#111827", anchor="w").pack(pady=(0, 10))

    from cart import set_cart_widgets
    set_cart_widgets(cart_list, total_label, discount_var)

    # Styled buttons
    tk.Button(cart_frame, text="Charge", bg="#0B6648", fg="#FFFFFF", font=("Arial", 10), width=20, command=charge).pack(pady=5)
    tk.Button(cart_frame, text="Remove Selected", bg="#922D2D", fg="#FFFFFF", font=("Arial", 10), width=20, command=remove_selected).pack(pady=5)

    quantity_btn_style = {"bg": "#D1D5DB", "fg": "#111827", "width": 5, "font": ("Arial", 10, "bold")}
    # Wrap + and - buttons in a horizontal frame
    qty_btn_frame = tk.Frame(cart_frame, bg="#FFFFFF")
    qty_btn_frame.pack(pady=5)

    tk.Button(qty_btn_frame, text="+", bg="#D1D5DB", fg="#111827", width=5, command=increase_quantity).pack(side="left", padx=5)
    tk.Button(qty_btn_frame, text="-", bg="#D1D5DB", fg="#111827", width=5, command=decrease_quantity).pack(side="left", padx=5)
    tk.Button(root, text="Logout", bg="lightgray", fg="black",
              command=lambda: show_login(root)).pack(anchor="ne", padx=10, pady=10)

    cart_list.bind("<Double-Button-1>", lambda e: remove_selected())

    # Initial Display
    display_products(product_frame, search_var)
