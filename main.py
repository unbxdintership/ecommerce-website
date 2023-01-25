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
        products=self.operator.get_random_products(9)
        categories=self.operator.get_catlevel1()
        return {"products":products,"categories":categories}
API.add_resource(Home, "/home")


class DB_Retrieve_Product(Resource):
    def __init__(self):
        self.retriever = DB_Operations()
    def get(self, product_ID):
        product = self.retriever.get_product(product_ID)
        categories=self.retriever.get_catlevel1()
        return {"product":product,"categories":categories}
API.add_resource(DB_Retrieve_Product, "/products/<string:product_ID>")

class DB_Retrieve_Random(Resource):
    def __init__(self):
        self.retriever = DB_Operations()
    def get(self):
        
        products = self.retriever.get_random_products(18)
        categories=self.retriever.get_catlevel1()
        return {"products":products,"categories":categories}
API.add_resource(DB_Retrieve_Random, "/products/")

class Product_Details(Resource):
    def __init__(self):
        self.get_cat = DB_Operations()
    def get(self, category_lvl1, category_lvl2):
        categories = self.get_cat.get_catlevel1()
        products = self.get_cat.get_category_lvl2_prods(category_lvl1, category_lvl2)
        return {"products":products,"categories":categories}
API.add_resource(Product_Details, "/category/<category_lvl1>/<category_lvl2>/")

class Product_Search(Resource):
    def __init__(self):
        self.URL = config.get('search_api', "URL")
        self.operator = DB_Operations()
    def get(self):
        # print(1111)
        categories=self.operator.get_catlevel1()
        rows = 10
        query = request.args.get('q')
        order=request.args.get('order')
        params = {
            "rows": rows,
            "q": query
        }
        if order=="Ascending":
            params["sort"]="price asc"
        elif order=="Descending":
            params["sort"]="price desc"
        else:
            pass
        response = requests.get(self.URL, params)
        products = response.json()
        # print(products)
        num_products = len(products["response"]["products"])
        #print(num_products)
        result = []
        for counter in range(0, num_products):
            result.append([
                products["response"]["products"][counter]["uniqueId"],
                products["response"]["products"][counter]["name"],
                products["response"]["products"][counter]["price"],
                products["response"]["products"][counter]["productDescription"],
                products["response"]["products"][counter]["productImage"]
            ])
            if self.operator.verify_product(products["response"]["products"][counter]["uniqueId"]) == 0:
                self.operator.insert_product(
                    products["response"]["products"][counter]["uniqueId"],
                    products["response"]["products"][counter]["title"],
                    products["response"]["products"][counter]["price"],
                    products["response"]["products"][counter]["productDescription"],
                    products["response"]["products"][counter]["productImage"],
                    products["response"]["products"][counter]["availability"],
                    products["response"]["products"][counter]["name"],
                    products["response"]["products"][counter]["catlevel1Name"],
                    products["response"]["products"][counter]["catlevel2Name"]
                )
        
        return {"products":result,"categories":categories}
API.add_resource(Product_Search, "/search")


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
                return {"Data Update": "Unsuccessful ❌"}
            else:
                product_ID = value.get("uniqueId")

            status = self.operator.verify_product(product_ID)
            if not status:
                print(
                    f"Product with ID: {product_ID} not present in the database.")
                return {"Data Update": "Unsuccessful ❌"}

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

        return {"Data Update": "Successful ✅"}
API.add_resource(DB_Ingest, "/ingestion")


# class Product_Sort_Asc(Resource):

#     def __init__(self):
#         self.URL = config.get('search_api', "URL")
#         self.operator = DB_Operations()

#     def get(self, query):
#         rows = 10
#         params = {
#             "q": query,
#             "rows": rows,
#             "sort": "price asc"
#         }
#         response = requests.get(self.URL, params)
#         products = response.json()
#         num_products = len(products["response"]["products"])
#         " = {
#":result}             "product_ID": [],
#             "product_title": [],
#             "product_image": [],
#             "product_name": [],
#             "product_price": [],
#             "product_availability": [],
#             "product_description": [],
#             "catlevel1": [],
#             "catlevel2": []
#         }
#         for counter in range(0, num_products):
#             result["product_ID"].append(
#                 products["response"]["products"][counter]["product_ID"])
#             result["product_title"].append(
#                 products["response"]["products"][counter]["product_title"])
#             result["product_image"].append(
#                 products["response"]["products"][counter]["product_image"])
#             result["product_name"].append(
#                 products["response"]["products"][counter]["product_name"])
#             result["product_price"].append(
#                 products["response"]["products"][counter]["product_price"])
#             result["product_availability"].append(
#                 products["response"]["products"][counter]["product_availability"])
#             result["product_description"].append(
#                 products["response"]["products"][counter]["product_description"])
#             result["catlevel1"].append(
#                 products["response"]["products"][counter]["catlevel1"])
#             result["catlevel2"].append(
#                 products["response"]["products"][counter]["catlevel2"])

#             if self.operator.verify_product(result["product_ID"][counter]):
#                 self.operator.insert_product(
#                     result["product_ID"][counter],
#                     result["product_title"][counter],
#                     result["product_price"][counter],
#                     result["product_description"][counter],
#                     result["product_image"][counter],
#                     result["product_availability"][counter],
#                     result["product_name"][counter],
#                     result["catlevel1"][counter],
#                     result["catlevel2"][counter]
#                 )

#         return result


# API.add_resource(Product_Sort_Asc, "/asort/<query>/")


# class Product_Sort_Desc(Resource):

#     def __init__(self):
#         self.URL = config.get('search_api', "URL")
#         self.operator = DB_Operations()

#     def get_products(self, query):
#         rows = 10
#         params = {
#             "q": query,
#             "rows": rows,
#             "sort": "price desc"
#         }
#         response = requests.get(self.URL, params)
#         products = response.json()
#         num_products = len(products["response"]["products"])
#         result = {
#             "product_ID": [],
#             "product_title": [],
#             "product_image": [],
#             "product_name": [],
#             "product_price": [],
#             "product_availability": [],
#             "product_description": [],
#             "catlevel1": [],
#             "catlevel2": []
#         }
#         for counter in range(0, num_products):
#             result["product_ID"].append(
#                 products["response"]["products"][counter]["product_ID"])
#             result["product_title"].append(
#                 products["response"]["products"][counter]["product_title"])
#             result["product_image"].append(
#                 products["response"]["products"][counter]["product_image"])
#             result["product_name"].append(
#                 products["response"]["products"][counter]["product_name"])
#             result["product_price"].append(
#                 products["response"]["products"][counter]["product_price"])
#             result["product_availability"].append(
#                 products["response"]["products"][counter]["product_availability"])
#             result["product_description"].append(
#                 products["response"]["products"][counter]["product_description"])
#             result["catlevel1"].append(
#                 products["response"]["products"][counter]["catlevel1"])
#             result["catlevel2"].append(
#                 products["response"]["products"][counter]["catlevel2"])

#             if self.operator.verify_product(result["product_ID"][counter]):
#                 self.operator.insert_product(
#                     result["product_ID"][counter],
#                     result["product_title"][counter],
#                     result["product_price"][counter],
#                     result["product_description"][counter],
#                     result["product_image"][counter],
#                     result["product_availability"][counter],
#                     result["product_name"][counter],
#                     result["catlevel1"][counter],
#                     result["catlevel2"][counter]
#                 )

#         return result


# API.add_resource(Product_Sort_Desc, "/dsort")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
