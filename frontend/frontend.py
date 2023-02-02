from flask import Flask, render_template, request
from configparser import ConfigParser
import requests

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)

print(config)

@app.route("/home/")
def home():
    domain = "http://be:3000/"
    final_domain = domain + "home/"
    response = requests.get(url=final_domain)
    data = response.json()
    products = data["products"]
    categories = data["categories"]
    return render_template("home.html", title="HomePage", categories=categories, products=products)


@app.route("/products/")
def render_products():
    page = int(request.args.get("page"))
    params = {"page": page}
    domain = "http://be:3000/"
    final_domain = domain + "products/"
    response = requests.get(url=final_domain, params=params)
    data = response.json()
    products = data["products"]
    categories = data["categories"]
    pages = data['pages']
    return render_template("products.html", products=products, categories=categories, page=page, pages=pages)


@app.route("/products/<product_id>/")
def render_product(product_id):
    domain = "http://be:3000/"
    final_domain = domain+f"products/{product_id}/"
    response = requests.get(url=final_domain)
    data = response.json()
    product = data['product']
    categories = data['categories']
    return render_template("product-details.html", product=product, categories=categories)


@app.route("/category/<catlvl1>/<catlvl2>/")
def render_catlvl2(catlvl1, catlvl2):
    page = int(request.args.get("page"))
    domain = "http://be:3000/"
    final_domain = domain + f"category/{catlvl1}/{catlvl2}/"
    response = requests.get(url=final_domain, params={"page": page})
    data = response.json()
    categories = data['categories']
    products = data['products']
    pages = data['pages']
    return render_template("category.html", catlevel1=catlvl1, catlevel2=catlvl2, categories=categories, products=products, page=page, pages=pages)


@app.route("/search/", methods=["GET", "POST"])
def render_query():
    page = int(request.args.get("page"))
    if request.method == "GET":
        query = request.args.get("query")
        order = request.args.get("order")
    if request.method == "POST":
        query = request.form.get("searchbar")
        order = request.form.get("sort-select")
    params = {
        "q": query,
        "order": order,
        "page": page
    }
    domain = "http://be:3000/"
    final_domain = domain + "search/"
    response = requests.get(url=final_domain, params=params)
    data = response.json()
    products = data['products']
    categories = data['categories']
    pages = data['pages']
    return render_template("search.html", products=products, categories=categories, pages=pages, page=page, query=query, order=order)

@app.route("/testing/")
def render_testing():
    return {"Testing": "Frontend"}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
