from flask import Flask
from flask_restful import Api, Resource
import configparser
from db_operations import DB_Operations

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
API = Api(app)

class Product_Details(Resource):

    def __init__(self):
        self.get_cat = DB_Operations()

    def get_products(self, category_ID):
        result = self.get_cat.get_category_details(category_ID)
        if result:
            return 1
API.add_resource(Product_Details, "/category/<string:category_ID>")
