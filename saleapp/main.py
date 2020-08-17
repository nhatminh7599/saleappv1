from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, session

from saleapp import app, dao, utils
import json
from saleapp.decorator import login_required


@app.route("/")
def init():
    return render_template("index.html")

@app.route("/products")
def product_list():
    kw = request.args["kw"] if request.args.get("kw") else None
    price_from = float(request.args["price_from"]) if request.args.get("price_from") else None
    price_to = float(request.args["price_to"]) if request.args.get("price_to") else None
    products = dao.read_product(kw=kw, price_from=price_from, price_to=price_to)
    return render_template('product-list.html', products=products)

@app.route("/products/<int:category_id>")
def product_list_by_cate_id(category_id):
    return render_template('product-list.html', products=dao.read_product_by_categoryid(category_id))

@app.route("/products/add", methods=["GET", "POST"])
@login_required
def product_add():
    err_msg = None
    if request.method == "POST":
        if request.args["product_id"] and int(request.args["product_id"]) > 0:
            p = dict(request.form.copy())
            p["id"] = request.args["product_id"]

            if dao.product_update(**p):
                return redirect(url_for('product_list'))
            else:
                pass
        else:
            if dao.product_add(**dict(request.form)):
                return redirect(url_for('product_list'))
            else:
                err_msg = "something wrong"
    product = None
    if request.args["product_id"]:
        if int(request.args["product_id"]) > 0:
            product = dao.read_product_by_id(int(request.args["product_id"]))
    categories = dao.read_categories()
    return render_template("product-add.html", categories=categories, err_msg=err_msg, product=product)

# @app.route("/products/delete")
# @login_required
# def product_delete():
#     if request.args["product_id"]:
#         if int(request.args["product_id"]) > 0:
#             dao.product_delete(request.args["product_id"])
#     return redirect(url_for('product_list'))

@app.route("/api/product/<int:product_id>", methods=["delete"])
@login_required
def product_delete_ajax(product_id):
    if dao.product_delete_ajax(product_id):
        return jsonify({"status": 200, "product_id": product_id})
    return jsonify({"status": 500})

@app.route("/products/export")
def product_export():
    p = utils.export()
    return send_file(filename_or_fp=p)

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.checklogin(username = username, password = password)
        if user:
            session["user"] = user
            if "next" in request.args:
                return redirect(request.args["next"])
            return redirect(url_for('init'))
    else:
        err_msg = "something wrong"
    return render_template("login.html", err_msg=err_msg)

@app.route("/logout")
def logout():
    if "user" in session:
        session["user"] = None
    return redirect(url_for("init"))

@app.route("/register", methods=["GET","POST"])
def register():
    if session.get("user"):
        redirect(request.url)
    err_msg = ''
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() != confirm.strip():
            err_msg = "Mat khau khong khop"
        else:
            if dao.adduser(name=name, username=username, password=password):
                return redirect(url_for('login'))
            else: err_msg = "something wrong"
    return render_template("register.html", err_msg=err_msg)

@app.route("/api/cart", methods=["post"])
def add_to_cart():
    data = json.loads(request.data)
    product_id = str(data.get("product_id"))
    name = data.get("name")
    price = data.get("price")
    if "cart" not in session:
        session["cart"] = {}
    cart = session["cart"]

    if product_id in cart:
        cart[product_id]["quantity"] = cart[product_id]["quantity"] + 1
    else:
        cart[product_id] = {
            "id": int(product_id),
            "name": name,
            "price": price,
            "quantity": 1
        }

    session["cart"] = cart

    return  jsonify({"success": 1, "quantity": sum([c["quantity"] for c in list(session["cart"].values())])})

@app.route("/payment")
def cart():
    return render_template("payment.html")

if __name__ == "__main__":
    app.run(debug=True);