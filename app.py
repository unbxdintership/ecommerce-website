from flask import Flask, render_template, request
from configparser import ConfigParser
from db_operations import DB_Operations


operator = DB_Operations()

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)

@app.route("/home/")
def home():
    products = operator.get_random_products(9)
    categories = operator.get_catlevel1()
    return render_template("home.html", title="HomePage", categories=categories, products=products)


@app.route("/products/<product_id>/")
def render_product(product_id):
    product = operator.get_product(product_id)
    categories = operator.get_catlevel1()
    return render_template("product-details.html", product=product, categories=categories)

@app.route("/category/<catlvl1>/<catlvl2>/")
def render_catlvl2(catlvl1, catlvl2):
    categories = operator.get_catlevel1()
    products = operator.get_category_lvl2_prods(catlvl1, catlvl2)
    return render_template("category.html", catlevel1=catlvl1, catlevel2=catlvl2, categories=categories, products=products)

@app.route("/products/")
def render_products():
    products = operator.get_random_products(18)
    categories = operator.get_catlevel1()
    return render_template("products.html", products=products, categories=categories)

@app.route("/search/", methods=["GET", "POST"])
def render_query():
    if request.method=="POST":
        query = request.form.get("searchbar")
        sort = request.form.get('sort-select')
    products = operator.get_search_products(query)
    categories = operator.get_catlevel1()
    return render_template("products.html", products=products, categories=categories)


# @app.route("/asort/")
# def render_asort():
#     pass

# @app.route("/dsort/")
# def render_asort():
#     pass

if __name__=="__main__":
    app.run(debug=True)
