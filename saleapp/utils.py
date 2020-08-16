from saleapp import dao, app
import os
import csv

def export():
    products = dao.read_product()
    path = os.path.join(app.root_path, 'data/products.csv')
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "description", "price", "image", "category_id"])
        writer.writeheader()
        for pro in products:
            writer.writerow(pro)
    return path


