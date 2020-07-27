from flask import Flask, render_template, request, redirect, url_for
from saleapp import app, dao

@app.route("/")
def init():
    return render_template('index.html')

@app.route("/products")
def product_list():
    kw = request.args["kw"] if request.args.get("kw") else None
    price_to = float(request.args["price_to"]) if request.args.get("price_to") else None
    price_end = float(request.args["price_end"]) if request.args.get("price_end") else None

    return render_template('product-list.html', products=dao.read_product(kw=kw, price_to=price_to, price_end=price_end))

@app.route("/products/<int:category_id>")
def product_list_by_cate_id(category_id):
    return render_template("product-list.html", products=dao.read_product_by_categoryid(category_id))

@app.route("/products/add", methods=["GET", "POST"])
def product_add():
    err_msg=None
    product=None
    if request.method == "POST":
        if dao.product_add(**dict(request.form)):
            return redirect(url_for('product_list'))
        else:
            err_msg = "something wrong"
    if request.args["product_id"]:
        product = dao.read_product_by_id(int(request.args["product_id"]))
    categories = dao.read_categories()
    return render_template("product-add.html", categories=categories, err_msg=err_msg, product=product)

if __name__ == "__main__":
    app.run(debug=True);