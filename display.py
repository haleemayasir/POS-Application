from tkinter import Frame, Label, Button
from PIL import Image, ImageTk, ImageEnhance
import os
from inventory import get_products
from cart import add_to_cart

products = get_products()
current_category = "Men"  # or "Women"

def switch_category(cat, frame, search_var):
    global current_category
    current_category = cat
    display_products(frame, search_var)

def load_image(file_name):
    try:
        img_path = os.path.join("images", file_name)
        img = Image.open(img_path).resize((140, 140), Image.LANCZOS)

        # Original image
        normal_img = ImageTk.PhotoImage(img)

        # Faded image (slightly dimmed)
        enhancer = ImageEnhance.Brightness(img)
        faded_img = ImageTk.PhotoImage(enhancer.enhance(0.8))

        return normal_img, faded_img
    except:
        print(f"Could not load image: {file_name}")
        return None, None

def display_products(product_frame, search_var):
    for widget in product_frame.winfo_children():
        widget.destroy()

    search_text = search_var.get().lower()
    row, col = 0, 0

    for product in products.get(current_category, []):
        if search_text in product["name"].lower():
            normal_img, faded_img = load_image(product["image"])
            if normal_img:
                item_frame = Frame(product_frame, bg="white")
                item_frame.grid(row=row, column=col, padx=20, pady=5)

                # Image as button
                btn = Button(item_frame, image=normal_img, command=lambda p=product: add_to_cart(p),
                        bd=0, bg="white", activebackground="white", cursor="hand2")
                btn.image = normal_img
                btn.normal_image = normal_img
                btn.faded_image = faded_img
                btn.pack()

                btn.bind("<Enter>", lambda e, b=btn: b.config(image=b.faded_image))
                btn.bind("<Leave>", lambda e, b=btn: b.config(image=b.normal_image))


                # Hover effect: fade in/out
                btn.bind("<Enter>", lambda e, b=btn: b.config(image=b.faded_image))
                btn.bind("<Leave>", lambda e, b=btn: b.config(image=b.normal_image))

                # Name and price under image
                Label(item_frame, text=product["name"], font=("Arial", 10, "bold"), bg="white").pack(pady=(5, 0))
                Label(item_frame, text=f"Rs {product['price']}", font=("Arial", 9), fg="green", bg="white").pack()

                col += 1
                if col >= 4:
                    col = 0
                    row += 1