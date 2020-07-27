import json
import os
from saleapp import app

def read_product(kw=None, price_to=None, price_end=None):
    with open(os.path.join(app.root_path, 'data/products.json'), encoding="utf-8") as p:
        products = json.load(p)
    if kw:
        return [product for product in products if product["name"].lower().find(kw.lower()) >= 0]
    if price_to and price_end:
        return [product for product in products if product["price"] >= price_to and product["price"] <= price_end]
    return products

def read_product_by_categoryid(category_id):
    products = read_product()
    return [product for product in products if product["category_id"] == category_id]
    # products = read_product()
    # res = []
    # for product in products:
    #     if(product["category_id"] == categoryid):
    #         res.append(product)
    # return res

def read_product_by_id(id):
    products = read_product()
    return [product for product in products if product["id"] == int(id)]

def product_add(name, description, price, image, category):
    products = read_product()
    products.append({
        "id": len(products) + 1,
        "name": name,
        "description": description,
        "price": float(price),
        "image": image,
        "category_id": float(category)
    })
    try:
        f = open(os.path.join(app.root_path, 'data/products.json',  encoding="utf-8"), "w", encoding="utf-8")
        json.dump(products, f, ensure_ascii=False, indent=4)
        f.close()
    except:
        ex = Exception
        return ex

def read_categories():
    with open(os.path.join(app.root_path, 'data/categories.json'), encoding="utf-8") as p:
        categories = json.load(p)
    return categories

if __name__ == "__main__":
    print(read_product())