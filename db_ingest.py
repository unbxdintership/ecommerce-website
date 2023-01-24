from flask import Flask, request
from flask_restful import  Api, Resource
from db_operations import DB_Operations

app = Flask(__name__)
API = Api(app)

class DB_Ingest(Resource):

    def __init__(self):
        self.operator = DB_Operations()

    def post(self):
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

            if ingestion_status==2:
                print(f"Product ID: {product_ID} already present.")
        
        if ingestion_status==1:
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
                print(f"Product with ID: {product_ID} not present in the database.")
                return {"Data Update": "Unsuccessful ❌"}

            if value.get("title") != None:
                self.operator.update_title(product_ID, value.get("title"))
                print("Updated title.")

            if value.get("price") != None:
                self.operator.update_price(product_ID, str(value.get("price")))
                print("Updated price.")

            if value.get("productDescription") != None:
                self.operator.update_description(product_ID, value.get("productDescription"))
                print("Updated desciption.")

            if value.get("productImage") != None:
                self.operator.update_image(product_ID, value.get("productImage"))
                print("Updated image.")

            if value.get("availability") != None:
                self.operator.update_availability(product_ID, value.get("availability"))
                print("Updated availability.")

            if value.get("name") != None:
                self.operator.update_name(product_ID, value.get("name"))
                print("Updated name.")
            
            print(f"Updated product with ID: {product_ID}.\n  *****")

        
        return {"Data Update": "Successful ✅"}
API.add_resource(DB_Ingest,"/ingestion")

if __name__ == "__main__":
    app.run(debug=True)