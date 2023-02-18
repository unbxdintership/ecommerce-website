'''
- handles the incoming request
- passes the reuired information about the request to the service
- gets the response from the service
- encodes the response
- returns response to user
'''

from flask_restful import Resource
from Service.product_details_service import ProductDetailsService


class ProductDetailsCntrl(Resource):
    def __init__(self):
        self.retriever = ProductDetailsService()

    def get(self, product_ID):
        product = self.retriever.get_product(product_ID)
        recommended_products = self.retriever.get_recommended_products(
            product_ID)
        return {"product": product, "recommend": recommended_products}
