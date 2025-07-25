from db import db_connect
db = db_connect()
cursor = db.cursor()

def get_products():
    
    cursor.execute("SELECT name, category, price, image, stock FROM inventory")
    rows = cursor.fetchall()
    
    products = {}
    for name, category, price, image, stock in rows:
        if category not in products:
            products[category] = []
        products[category].append({
            "name": name,
            "price": price,
            "image": image,
            "stock": stock
        })
    
    return products
