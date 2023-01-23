from flask import Flask
from flask_restful import Api, Resource
from db_operations import DB_Operations

app = Flask(__name__)
API = Api(app)

class DB_Retrieve_Product(Resource):

    def __init__(self):
        self.retriever = DB_Operations()

    def get(self, product_ID):
        product = self.retriever.get_product(product_ID)
        return product
API.add_resource(DB_Retrieve_Product, "/products/<string:product_ID>/")

class DB_Retrieve_Random(Resource):
    def __init__(self):
        self.retriever = DB_Operations()

    def get(self):
        products = self.retriever.get_random_products()
        return products
API.add_resource(DB_Retrieve_Random, "/products/")