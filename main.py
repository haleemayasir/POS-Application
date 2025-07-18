import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Define product data with categories
products = {
    "Sweets": [
        {"name": "Donut", "price": 2.50, "image": "donut.png"},
        {"name": "Chocolate Cake", "price": 3.00, "image": "chocolate cake.png"},
        {"name": "Brownie", "price": 2.75, "image": "brownie.png"},
        {"name": "Cupcake", "price": 2.90, "image": "cupcake.png"},
        {"name": "Macaron", "price": 3.20, "image": "macaron.png"},
        {"name": "Cookie", "price": 1.99, "image": "cookie.png"},
        {"name": "Pudding", "price": 2.60, "image": "pudding.png"},
        {"name": "Muffin", "price": 2.80, "image": "muffin.png"},
        {"name": "Churros", "price": 3.50, "image": "churros.png"},
        {"name": "Tart", "price": 3.10, "image": "tart.png"},
        {"name": "Ice Cream", "price": 3.00, "image": "icecream.png"},
        {"name": "Donut Ball", "price": 2.20, "image": "donutball.png"},
    ],
    "Spicy": [
        {"name": "Burger", "price": 5.99, "image": "burger.png"},
        {"name": "Soup", "price": 2.99, "image": "soup.png"},
        {"name": "Noodles", "price": 6.50, "image": "noodles.png"},
        {"name": "Sushi", "price": 4.20, "image": "sushi.png"},
        {"name": "Hot Dog", "price": 4.99, "image": "hotdog.png"},
        {"name": "Tacos", "price": 5.40, "image": "tacos.png"},
        {"name": "Shawarma", "price": 6.20, "image": "shawarma.png"},
        {"name": "Wrap", "price": 5.30, "image": "wrap.png"},
        {"name": "Popcorn Chicken", "price": 4.75, "image": "popcornchicken.png"},
        {"name": "Wings", "price": 5.80, "image": "wings.png"},
        {"name": "Kebab", "price": 6.00, "image": "kebab.png"},
        {"name": "Spicy Rice", "price": 4.99, "image": "spicyrice.png"},
    ],
    "Drinks": [
        {"name": "Coke", "price": 1.50, "image": "coke.png"},
        {"name": "Pepsi", "price": 1.50, "image": "pepsi.png"},
        {"name": "Orange Juice", "price": 2.00, "image": "orangejuice.png"},
        {"name": "Water", "price": 1.00, "image": "water.png"},
        {"name": "Milkshake", "price": 2.50, "image": "milkshake.png"},
        {"name": "Iced Tea", "price": 2.25, "image": "icedtea.png"},
        {"name": "Cappuccino", "price": 2.75, "image": "Cappuccino.png"},
        {"name": "Lemonade", "price": 2.10, "image": "lemonade.png"},
        {"name": "Smoothie", "price": 3.00, "image": "smoothie.png"},
        {"name": "Energy Drink", "price": 2.60, "image": "energydrink.png"},
        {"name": "Strawberry Shake", "price": 2.80, "image": "strawberryshake.png"},
        {"name": "Blueberry Cooler", "price": 2.90, "image": "blueberrycooler.png"},
    ]
}
cart = []
TAX_RATE = 0.08      # 8% tax
DISC_RATE = 0.10     # 10% discount
current_category = "Spicy"

# --- Functions ---

def load_image(file_name):
    try:
        img_path = os.path.join("images", file_name)
        img = Image.open(img_path)
        img = img.resize((100, 100))
        return ImageTk.PhotoImage(img)
    except:
        return None

def switch_category(cat):
    global current_category
    current_category = cat
    display_products()

def display_products():
    for widget in product_frame.winfo_children():
        widget.destroy()
    for product in products[current_category]:
        img = load_image(product["image"])
        if img:
            btn = tk.Button(product_frame, image=img, command=lambda p=product: add_to_cart(p))
            btn.image = img  # Keep a reference!
            btn.pack(side="left", padx=10, pady=10)

def add_to_cart(product):
    cart.append(product)
    update_cart()

def update_cart():
    cart_list.delete(0, tk.END)
    subtotal = 0
    for item in cart:
        cart_list.insert(tk.END, f"{item['name']} — ${item['price']:.2f}")
        subtotal += item['price']

    discount = subtotal * DISC_RATE if discount_var.get() else 0  # NEW
    taxed    = (subtotal - discount) * TAX_RATE                  # NEW
    total    = subtotal - discount + taxed                       # NEW

    total_label.config(text=(f"Subtotal: ${subtotal:.2f}\n"
                             f"Discount: -${discount:.2f}\n"
                             f"Tax (8%): +${taxed:.2f}\n"
                             f"Total: ${total:.2f}"))

def charge():
    if not cart:
        messagebox.showwarning("Cart Empty", "Please add items to cart.")
        return

    subtotal = sum(i['price'] for i in cart)
    discount = subtotal * DISC_RATE if discount_var.get() else 0
    taxed    = (subtotal - discount) * TAX_RATE
    total    = subtotal - discount + taxed

    # Create fancy receipt text
    slip = "       ✦ RECEIPT ✦\n"
    slip += "-" * 26 + "\n"
    for item in cart:
        slip += f"{item['name']:<18}${item['price']:>5.2f}\n"
    slip += "-" * 26 + "\n"
    slip += f"{'Subtotal':<18}${subtotal:>5.2f}\n"
    if discount:
        slip += f"{'Discount':<18}-${discount:>5.2f}\n"
    slip += f"{'Tax (8%)':<18}+${taxed:>5.2f}\n"
    slip += f"{'TOTAL':<18}${total:>5.2f}\n"
    slip += "-" * 26 + "\nThank you for shopping!\n"

    messagebox.showinfo("Order Placed", slip)

    cart.clear()
    discount_var.set(False)  # uncheck discount for next customer
    update_cart()

def remove_selected():
    selected = cart_list.curselection()
    if selected:
        index = selected[0]
        del cart[index]
        update_cart()

# --- GUI ---

root = tk.Tk()
root.title("POS App with Categories")
root.geometry("900x600")

# Category Buttons
category_frame = tk.Frame(root)
category_frame.pack(pady=10)

for cat in products:
    btn = tk.Button(category_frame, text=cat, command=lambda c=cat: switch_category(c))
    btn.pack(side="left", padx=10)

# Product Display Frame
product_frame = tk.Frame(root)
product_frame.pack(pady=10)

# Cart and Checkout
cart_frame = tk.Frame(root)
cart_frame.place(x=700, y=20)  # NEW: Positions cart at the top-right corner


tk.Label(cart_frame, text="Cart", font=("Arial", 14, "bold")).pack()

cart_list = tk.Listbox(cart_frame, width=30, height=20)
cart_list.pack()

total_label = tk.Label(cart_frame, text="Total: $0.00", font=("Arial", 12))
total_label.pack(pady=5)
discount_var = tk.BooleanVar()  # NEW
tk.Checkbutton(cart_frame, text="Apply 10% discount",
               variable=discount_var, command=update_cart).pack()  # NEW

tk.Button(cart_frame, text="Charge", bg="green", fg="white", width=20, command=charge).pack(pady=10)
tk.Button(cart_frame, text="Remove Selected", bg="red", fg="white",  # NEW
          width=20, command=lambda: remove_selected()).pack(pady=5)
cart_list.bind("<Double-Button-1>", lambda e: remove_selected())  # NEW

# Show default category
display_products()

root.mainloop()
