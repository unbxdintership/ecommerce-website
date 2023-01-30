from flask import Flask, request
from flask_restful import Api, Resource
import configparser
from db_operations import DB_Operations
import requests
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
API = Api(app)


class Home(Resource):
    def __init__(self):
        self.operator = DB_Operations()

    def get(self):
        products = self.operator.get_random_products(18)
        categories = self.operator.get_catlevel1()
        return {"products": products, "categories": categories}
API.add_resource(Home, "/home")


class DB_Retrieve_Product(Resource):
    def __init__(self):
        self.retriever = DB_Operations()

    def get(self, product_ID):
        product = self.retriever.get_product(product_ID)
        categories = self.retriever.get_catlevel1()
        return {"product": product, "categories": categories}
API.add_resource(DB_Retrieve_Product, "/products/<string:product_ID>/")


class DB_Retrieve_Random(Resource):
    def __init__(self):
        self.retriever = DB_Operations()

    def get(self):
        page = int(request.args.get("page"))
        all_products = self.retriever.get_random_products()
        products_length = len(all_products)
        pages = products_length//18
        if (products_length%18)!=0:
            pages+=1
        start, end = (page-1)*18, (page-1)*18+18
        if end>=products_length:
            end = products_length
        products = all_products[start: end]
        categories = self.retriever.get_catlevel1()
        return {"products": products, "categories": categories, "pages": pages, "page": page}
API.add_resource(DB_Retrieve_Random, "/products/")


class Product_Details(Resource):
    def __init__(self):
        self.get_cat = DB_Operations()

    def get(self, category_lvl1, category_lvl2):
        page = int(request.args.get("page"))
        categories = self.get_cat.get_catlevel1()
        status = self.get_cat.get_redis_products(category_lvl1, category_lvl2)
        if status == 1:
            all_products = self.get_cat.get_category_lvl2_prods(
                category_lvl1, category_lvl2)
            status1 = self.get_cat.insert_redis_products(category_lvl1, category_lvl2, all_products)
            if status1 == 1:
                print("Inserted into redis...")
        else:
            all_products = status
        products_length = len(all_products)
        pages = products_length//18
        if (products_length%18)!=0:
            pages+=1
        start, end = (page-1)*18, (page-1)*18+18
        if end>=products_length:
            end = products_length
        products = all_products[start: end]
        return {"products": products, "categories": categories, "pages": pages, "page": page}
API.add_resource(Product_Details, "/category/<category_lvl1>/<category_lvl2>/")


class Product_Search(Resource):
    def __init__(self):
        self.URL = config.get('search_api', "URL")
        self.operator = DB_Operations()

    def get(self):
        page = int(request.args.get("page"))
        categories = self.operator.get_catlevel1()
        query = request.args.get('q')
        order = request.args.get('order')
        params = {
            "q": query
        }
        if order == "Ascending":
            params["sort"] = "price asc"
        elif order == "Descending":
            params["sort"] = "price desc"
        # status = self.operator.get_redis_products(params)
        # if status == 1:
        all_result = self.operator.get_search_products(query, order)
        #     status1 = self.operator.insert_redis_products(params, all_result)
        #     if status1 == 1:
        #         print("Inserted into redis...")
        # else:
        #     all_result = status
        products_length = len(all_result)
        pages = products_length//18
        if (products_length%18)!=0:
            pages+=1
        start, end = (page-1)*18, (page-1)*18+18
        if end>=products_length:
            end = products_length
        products = all_result[start: end]
        return {"products": products, "categories": categories, "pages": pages, "page": page}
API.add_resource(Product_Search, "/search/")


class DB_Ingest(Resource):
    def __init__(self):
        self.operator = DB_Operations()

    def post(self):
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

            ingestion_status = self.operator.insert_product(
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

    def put(self):
        product = request.json
        for value in product:
            if value.get("uniqueId") == None:
                print("Product ID not mentioned.")
                return {"Data Update": "Unsuccessful"}
            else:
                product_ID = value.get("uniqueId")

            status = self.operator.verify_product(product_ID)
            if not status:
                print(
                    f"Product with ID: {product_ID} not present in the database.")
                return {"Data Update": "Unsuccessful"}

            if value.get("title") != None:
                self.operator.update_title(product_ID, value.get("title"))
                print("Updated title.")

            if value.get("price") != None:
                self.operator.update_price(product_ID, str(value.get("price")))
                print("Updated price.")

            if value.get("productDescription") != None:
                self.operator.update_description(
                    product_ID, value.get("productDescription"))
                print("Updated desciption.")

            if value.get("productImage") != None:
                self.operator.update_image(
                    product_ID, value.get("productImage"))
                print("Updated image.")

            if value.get("availability") != None:
                self.operator.update_availability(
                    product_ID, value.get("availability"))
                print("Updated availability.")

            if value.get("name") != None:
                self.operator.update_name(product_ID, value.get("name"))
                print("Updated name.")

            print(f"Updated product with ID: {product_ID}.\n  *****")
        return {"Data Update": "Successful"}
API.add_resource(DB_Ingest, "/ingestion/")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
