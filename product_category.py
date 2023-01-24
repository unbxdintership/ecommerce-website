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

    def get(self, category_lvl1, category_lvl2):
        result = self.get_cat.get_category_details(category_lvl1, category_lvl2)
        print(result)
        if result:
            return result
API.add_resource(Product_Details, "/category/<category_lvl1>/<category_lvl2>/")

if __name__=="__main__":
    app.run(debug=True)
