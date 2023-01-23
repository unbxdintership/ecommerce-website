import requests
import configparser
from flask import Flask, request
from flask_restful import Api, Resource
from db_operations import DB_Operations

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
API = Api(app)

class Product_Search(Resource):

    def __init__(self):
        self.URL = config.get('search_api', "URL")
        self.operator = DB_Operations()

    def get(self, query):
        rows = 10
        params = {
            "q": query,
            "rows": rows
        }
        response = requests.get(self.URL, params)
        products = response.json()
        num_products = len(products["response"]["products"])
        result = {
            "product_ID": [],
            "product_title": [],
            "product_image": [],
            "product_name": [],
            "product_price": [],
            "product_availability": [],
            "product_description": [],
            "catlevel1": [],
            "catlevel2": []
        }
        for counter in range(0, num_products):
            result["product_ID"].append(products["response"]["products"][counter]["product_ID"]) 
            result["product_title"].append(products["response"]["products"][counter]["product_title"])
            result["product_image"].append(products["response"]["products"][counter]["product_image"])
            result["product_name"].append(products["response"]["products"][counter]["product_name"])
            result["product_price"].append(products["response"]["products"][counter]["product_price"])
            result["product_availability"].append(products["response"]["products"][counter]["product_availability"])
            result["product_description"].append(products["response"]["products"][counter]["product_description"])
            result["catlevel1"].append(products["response"]["products"][counter]["catlevel1"])
            result["catlevel2"].append(products["response"]["products"][counter]["catlevel2"])

            if self.operator.verify_product(result["product_ID"][counter]):
                self.operator.insert_product(
                    result["product_ID"][counter],
                    result["product_title"][counter],
                    result["product_price"][counter],
                    result["product_description"][counter],
                    result["product_image"][counter],
                    result["product_availability"][counter],
                    result["product_name"][counter],
                    result["catlevel1"][counter],
                    result["catlevel2"][counter]
                )
        
        return result
API.add_resource(Product_Search, "/search/<string:query>")

if __name__=="__main__":
    app.run(debug=True)