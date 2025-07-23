from tkinter import Frame, Label, Button
from PIL import Image, ImageTk
import os
from inventory import products
from shared import product_frame, search_var, current_category
from cart import add_to_cart


def switch_category(cat):
    global current_category
    current_category = cat
    display_products()

def load_image(file_name):
    try:
        img_path = os.path.join("images", file_name)
        img = Image.open(img_path)
        img = img.resize((100, 100))
        return ImageTk.PhotoImage(img)
    except:
        return None

def display_products():
    for widget in product_frame.winfo_children():
        widget.destroy()

    search_text = search_var.get().lower()
    row, col = 0, 0

    for product in products[current_category]:
        if search_text in product["name"].lower():
            img = load_image(product["image"])
            if img:
                item_frame = Frame(product_frame)
                item_frame.grid(row=row, column=col, padx=10, pady=10)

                btn = Button(item_frame, image=img, command=lambda p=product: add_to_cart(p))
                btn.image = img
                btn.pack()
                Label(item_frame, text=product["name"]).pack()

                col += 1
                if col >= 4:
                    col = 0
                    row += 1
