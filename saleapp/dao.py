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

if __name__ == "__main__":
    print(read_product())