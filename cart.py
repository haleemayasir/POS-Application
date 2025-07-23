from tkinter import messagebox
from shared import cart_list, total_label, discount_var
from inventory import products

cart = []
TAX_RATE = 0.08
DISC_RATE = 0.10

def add_to_cart(product):
    cart.append(product)
    update_cart()

def update_cart():
    cart_list.delete(0, "end")
    subtotal = sum(item["price"] for item in cart)
    discount = subtotal * DISC_RATE if discount_var.get() else 0
    taxed = (subtotal - discount) * TAX_RATE
    total = subtotal - discount + taxed

    for item in cart:
        cart_list.insert("end", f"{item['name']} — ${item['price']:.2f}")

    total_label.config(text=f"Subtotal: ${subtotal:.2f}\n"
                            f"Discount: -${discount:.2f}\n"
                            f"Tax (8%): +${taxed:.2f}\n"
                            f"Total: ${total:.2f}")

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
    discount_var.set(False)
    update_cart()

def remove_selected():
    selected = cart_list.curselection()
    if selected:
        del cart[selected[0]]
        update_cart()
