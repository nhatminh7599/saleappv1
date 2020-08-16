import json, csv, hashlib
import os
from saleapp import app
from functools import wraps

def read_product(kw=None, price_from=None, price_to=None):
    with open(os.path.join(app.root_path, 'data/products.json'), encoding="utf-8") as p:
        products = json.load(p)
    if kw:
        return [product for product in products if product["name"].lower().find(kw.lower()) >= 0]
    if price_from and price_to:
        return [product for product in products if product["price"] >= price_from and product["price"] <= price_to]
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
    # return [product for product in products if product["id"] == int(id)]
    products = read_product()
    res = None
    for product in products:
        if(product["id"] == int(id)):
            res = product
    return res

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
        f = open(os.path.join(app.root_path, 'data/products.json'), "w", encoding="utf-8")
        json.dump(products, f, ensure_ascii=False, indent=4)
        f.close()
        return True
    except Exception as ex:
        print(ex)
        return False

def product_update_json(products):
    try:
        f = open(os.path.join(app.root_path, 'data/products.json'), "w", encoding="utf-8")
        json.dump(products, f, ensure_ascii=False, indent=4)
        f.close()
        return True
    except Exception as ex:
        print(ex)
        return False

def product_update(id, name, description, price, image, category):
    products = read_product()
    for pro in products:
        if pro["id"] == int(id):
            pro["name"] = name
            pro["description"] = description
            pro["price"] = float(price)
            pro["image"] = image
            pro["category"] = int(category)
            break
    return product_update_json(products)

def product_delete(id):
    products = read_product()
    for pro in products:
        if pro["id"] == int(id):
            products.remove(pro)
            break
    return product_update_json(products)

def product_delete_ajax(product_id):
    products = read_product()
    for idx,pro in enumerate(products):
        if pro["id"] == int(product_id):
            del products[idx]
            break
    return product_update_json(products)


def read_csv():
    path = os.path.join(app.root_path, 'data/products.csv')
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
    return reader


def read_categories():
    with open(os.path.join(app.root_path, 'data/categories.json'), encoding="utf-8") as p:
        categories = json.load(p)
    return categories

def load_user():
    with open(os.path.join(app.root_path, "data/users.json"), encoding="utf-8") as f:
        return json.load(f)

def checklogin(username, password):
    users = load_user()
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    for u in users:
        if u["username"].strip() == username.strip() and u["password"] == password:
            return u

def adduser(name, username, password):
    users = load_user()
    users.append({
        "id": len(users) + 1,
        "name": name.strip(),
        "username": username.strip(),
        "password": str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    })
    f = open(os.path.join(app.root_path, 'data/users.json'), "w", encoding="utf-8")
    json.dump(users, f, ensure_ascii=False, indent=4)
    f.close()
    return True

if __name__ == "__main__":
    print(read_product())