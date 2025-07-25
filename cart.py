from tkinter import messagebox

cart = {} 
TAX_RATE = 0.08
DISC_RATE = 0.10

cart_list = None
total_label = None
discount_var = None

def set_cart_widgets(listbox, label, discount):
    global cart_list, total_label, discount_var
    cart_list = listbox
    total_label = label
    discount_var = discount

def add_to_cart(product):
    name = product["name"]
    if name in cart:
        cart[name]["qty"] += 1
    else:
        cart[name] = {"product": product, "qty": 1}
    update_cart()

def update_cart():
    if not cart_list or not total_label or discount_var is None:
        return

    cart_list.delete(0, "end")
    subtotal = 0

    for name, data in cart.items():
        item = data["product"]
        qty = data["qty"]
        price = item["price"] * qty
        subtotal += price
        cart_list.insert("end", f"{qty}x {name} — Rs {price:.2f}")

    discount = subtotal * DISC_RATE if discount_var.get() else 0
    taxed = (subtotal - discount) * TAX_RATE
    total = subtotal - discount + taxed

    total_label.config(text=f"Subtotal: Rs {subtotal:.2f}\n"
                            f"Discount: -Rs {discount:.2f}\n"
                            f"Tax (8%): +Rs {taxed:.2f}\n"
                            f"Total: Rs {total:.2f}")

def charge():
    if not cart:
        messagebox.showwarning("Cart Empty", "Please add items to the cart.")
        return

    subtotal = sum(i['price'] for i in cart)
    discount = subtotal * DISC_RATE if discount_var.get() else 0
    taxed = (subtotal - discount) * TAX_RATE
    total = subtotal - discount + taxed

    slip = "       ✦ RECEIPT ✦\n"
    slip += "-" * 26 + "\n"
    for item in cart:
        slip += f"{item['name']:<18}Rs {item['price']:>5.2f}\n"
    slip += "-" * 26 + "\n"
    slip += f"{'Subtotal':<18}Rs {subtotal:>5.2f}\n"
    if discount:
        slip += f"{'Discount':<18}-Rs {discount:>5.2f}\n"
    slip += f"{'Tax (8%)':<18}+Rs {taxed:>5.2f}\n"
    slip += f"{'TOTAL':<18}Rs {total:>5.2f}\n"
    slip += "-" * 26 + "\nThank you for shopping!\n"

    messagebox.showinfo("Order Placed", slip)
    cart.clear()
    discount_var.set(False)
    update_cart()

def remove_selected():
    selected = cart_list.curselection()
    if selected:
        del cart[selected[0]]
        update_cart()

def increase_quantity():
    selected = cart_list.curselection()
    if selected:
        name = cart_list.get(selected[0]).split("x ")[1].split(" —")[0]
        if name in cart:
            cart[name]["qty"] += 1
            update_cart()

def decrease_quantity():
    selected = cart_list.curselection()
    if selected:
        name = cart_list.get(selected[0]).split("x ")[1].split(" —")[0]
        if name in cart:
            cart[name]["qty"] -= 1
            if cart[name]["qty"] <= 0:
                del cart[name]
            update_cart()

