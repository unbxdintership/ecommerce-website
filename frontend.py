from flask import Flask, render_template, request
from configparser import ConfigParser
from db_operations import DB_Operations
import requests


operator = DB_Operations()

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)

@app.route("/home/")
def home():
    domain = config.get("backend", "URL")
    final_domain = domain + "home"
    data = requests.get(url=final_domain)
    response = data.json()
    products = response["products"]
    categories = response["categories"]
    return render_template("home.html", title="HomePage", categories=categories, products=products)

@app.route("/products/")
def render_products():
    domain = config.get("backend", "URL")
    final_domain = domain + "/products"
    data = requests.get(url=final_domain)
    response = data.json()
    products = response["products"]
    categories = response["categories"]
    return render_template("products.html", products=products, categories=categories)

@app.route("/ingestion/", methods={'POST', 'PUT'})
def ingest_products():
    domain = config.get("backend", "URL")
    final_domain = domain + "/ingestion"
    if request.method == 'POST':
        data = request.json
        response = requests.post(url=final_domain, json=data)
        print(response)
    
    elif request.method=="PUT":
        product = request.json
        for value in product:
            response = requests.put(url=final_domain, data=value)
            print(response)
    return response
    return {"ingestion":"successfull"}
@app.route("/products/<product_id>/")
def render_product(product_id):
    domain = config.get("backend", "URL")
    final_domain = domain+f"/products/{product_id}"
    response = requests.get(url=final_domain)
    data = response.json()
    product = data['product']
    categories = data['categories']
    return render_template("product-details.html", product=product, categories=categories)


@app.route("/category/<catlvl1>/<catlvl2>/")
def render_catlvl2(catlvl1, catlvl2):
    domain = config.get("backend", "URL")
    final_domain = domain + f"category/{catlvl1}/{catlvl2}"
    response = requests.get(url=final_domain)
    data = response.json()
    categories = data['categories']
    products = data['products']
    return render_template("category.html", catlevel1=catlvl1, catlevel2=catlvl2, categories=categories, products=products)

@app.route("/search/", methods=["GET", "POST"])
def render_query():
    if request.method=="POST":
        query = request.form.get("searchbar")
        order = request.form.get("sort-select")
    params = {
        "q": query,
        "order": order
    }
    domain = config.get("backend", "URL")
    final_domain = domain + "search"
    response = requests.get(url=final_domain, params=params)
    data = response.json()
    products = data['products']
    categories = data['categories']
    return render_template("products.html", products=products, categories=categories)   


if __name__ == "__main__":
    app.run(debug=True)
