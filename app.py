from flask import Flask, render_template,request
from flask_restful import Api, Resource
import requests
from db_operations import DB_Operations
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

operator=DB_Operations()
app = Flask(__name__)
API = Api(app)

# categories = {
#     "men": [
#         'Pant',
#         'Shirt',
#         'Caps'
#     ],
#     "women": [
#         'Tops',
#         'Dresses',
#         'Earrings'
#     ]
# }

# products = [
#     ['Top', '25', 'https://www.w3schools.com/images/lamp.jpg'],
#     ['Top', '25', 'https://www.w3schools.com/images/lamp.jpg'],
#     ['Top', '25', 'https://www.w3schools.com/images/lamp.jpg'],
#     ['Top', '25', 'https://www.w3schools.com/images/lamp.jpg'],
#     ['Top', '25', 'https://www.w3schools.com/images/lamp.jpg'],
#     ['Top', '25', 'https://www.w3schools.com/images/lamp.jpg'],
#     ['Top', '25', 'https://www.w3schools.com/images/lamp.jpg'],
#     ['Top', '25', 'https://www.w3schools.com/images/lamp.jpg'],
#     ['Top', '25', 'https://www.w3schools.com/images/lamp.jpg']
# ]


@app.route("/home/")
def home():
    # return render_template("home.html", title="HomePage", categories=categories)
    products=operator.get_random_products()

    categories=operator.get_catlevel1()
    
    #print(categories)
    return render_template("home.html", title="HomePage", categories=categories, products=products)

# class Home(Resource):
#     def get(self):
#         return render_template("home.html", title="HomePage", categories=categories, products=products)
# API.add_resource(Home, "/home/")


@app.route("/products/<product_id>/")
def render_product(product_id):
    
    # product_name, product_price, product_url, product_description = products[0][0], products[0][1], products[0][2], "This is a very nice top which looks like a lightbulb."
    
    #product = [products[0][0], products[0][1], products[0][2], "This is a very nice top which looks like a lightbulb."]
    product=operator.get_product(product_id)
    categories=operator.get_catlevel1()
    print(product)
    return render_template("product-details.html", product=product, categories=categories)

@app.route("/category/<catlvl1>/<catlvl2>/")
def render_catlvl2(catlvl1, catlvl2):
    products=operator.get_category_lvl2_prods(catlvl1,catlvl2)
    categories=operator.get_catlevel1()
    #products=
    return render_template("category.html", catlevel1=catlvl1, catlevel2=catlvl2, categories=categories, products=products)

@app.route("/products/")
def render_products():
    categories=operator.get_catlevel1()
    products=operator.get_random_products()
    return render_template("products.html", products=products, categories=categories)

    
@app.route("/search",methods =["GET", "POST"])
def render_query():
    categories=operator.get_catlevel1() 
    if request.method=="POST":
        
    
        
        query=request.form.get("search")
        print(query)
        products=operator.search_products(query)
    return render_template("products.html", products=products,categories=categories)
# @app.route("/asort/")
# def render_asort():
#     pass

# @app.route("/dsort/")
# def render_asort():
#     pass

if __name__=="__main__":
    app.run(debug=True)
