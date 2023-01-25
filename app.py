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
    categories = operator.get_catlevel1()
    if request.method == "POST":
        query = request.form.get("searchbar")
        order = request.form.get('sort-select')
        products = operator.get_search_products(query, order)
    return render_template("products.html", products=products, categories=categories)

@app.route("/ingestion",methods=["POST","PUT"])
def ingest_product():
    if request.method=="POST":
            data=request.json
            for product in data:
                product_ID = product['uniqueId']
                product_title = product['title']
                product_price = product['price']
                product_description = product.get('productDescription', "")
                product_image = product['productImage']
                product_avail = product['availability']
                product_name = product['name']
                product_catlevel1 = product['catlevel1Name']
                product_catlevel2 = product.get('catlevel2Name', "")
            
                ingestion_status = operator.insert_product(
                    product_ID,
                    product_title,
                    product_price,
                    product_description,
                    product_image,
                    product_avail,
                    product_name,
                    product_catlevel1,
                    product_catlevel2
                )

                if ingestion_status==2:
                    print(f"Product ID: {product_ID} already present.")
            
            if ingestion_status==1:
                return {"Data Ingestion": "Successful"}
            else:
                return {"Data Ingestion": "Unsuccessful"}
    elif request.method=="PUT":
        product = request.json
        for value in product:
            if value.get("uniqueId") == None:
                print("Product ID not mentioned.")
                return {"Data Update": "Unsuccessful ❌"}
            else:
                product_ID = value.get("uniqueId")

            status = operator.verify_product(product_ID)
            if not status:
                print(f"Product with ID: {product_ID} not present in the database.")
                return {"Data Update": "Unsuccessful ❌"}

            if value.get("title") != None:
                operator.update_title(product_ID, value.get("title"))
                print("Updated title.")

            if value.get("price") != None:
                operator.update_price(product_ID, str(value.get("price")))
                print("Updated price.")

            if value.get("productDescription") != None:
                operator.update_description(product_ID, value.get("productDescription"))
                print("Updated desciption.")

            if value.get("productImage") != None:
                operator.update_image(product_ID, value.get("productImage"))
                print("Updated image.")

            if value.get("availability") != None:
                operator.update_availability(product_ID, value.get("availability"))
                print("Updated availability.")

            if value.get("name") != None:
                operator.update_name(product_ID, value.get("name"))
                print("Updated name.")
            
            print(f"Updated product with ID: {product_ID}.\n  *****")

        
        return {"Data Update": "Successful ✅"}        


@app.route("/ingestion", methods={'POST', 'PUT'})
def ingest_products():
    if request.method == 'POST':
        data = request.json
        for product in data:
            product_ID = product['uniqueId']
            product_title = product['title']
            product_price = product['price']
            product_description = product.get('productDescription', "")
            product_image = product['productImage']
            product_avail = product['availability']
            product_name = product['name']
            product_catlevel1 = product['catlevel1Name']
            product_catlevel2 = product.get('catlevel2Name', "")

            ingestion_status = operator.insert_product(
                product_ID,
                product_title,
                product_price,
                product_description,
                product_image,
                product_avail,
                product_name,
                product_catlevel1,
                product_catlevel2
            )

            if ingestion_status == 2:
                print(f"Product ID: {product_ID} already present.")

        if ingestion_status == 1:
            return {"Data Ingestion": "Successful"}
        else:
            return {"Data Ingestion": "Unsuccessful"}

    elif request.method=="PUT":
        product = request.json
        for value in product:
            if value.get("uniqueId") == None:
                print("Product ID not mentioned.")
                return {"Data Update": "Unsuccessful"}
            else:
                product_ID = value.get("uniqueId")

            status = operator.verify_product(product_ID)
            if not status:
                print(f"Product with ID: {product_ID} not present in the database.")
                return {"Data Update": "Unsuccessful"}

            if value.get("title") != None:
                operator.update_title(product_ID, value.get("title"))
                print("Updated title.")

            if value.get("price") != None:
                operator.update_price(product_ID, str(value.get("price")))
                print("Updated price.")

            if value.get("productDescription") != None:
                operator.update_description(product_ID, value.get("productDescription"))
                print("Updated desciption.")

            if value.get("productImage") != None:
                operator.update_image(product_ID, value.get("productImage"))
                print("Updated image.")

            if value.get("availability") != None:
                operator.update_availability(product_ID, value.get("availability"))
                print("Updated availability.")

            if value.get("name") != None:
                operator.update_name(product_ID, value.get("name"))
                print("Updated name.")
            
            print(f"Updated product with ID: {product_ID}.\n  *****")

        
        return {"Data Update": "Successful"}


if __name__ == "__main__":
    app.run(debug=True)
