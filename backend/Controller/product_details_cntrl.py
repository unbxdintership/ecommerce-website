from flask_restful import Resource
from Service.product_details_service import ProductDetailsService


class ProductDetailsCntrl(Resource):
    def __init__(self):
        self.retriever = ProductDetailsService()

    def get(self, product_ID):
        product = self.retriever.get_product(product_ID)
        recommendedproduct = self.retriever.get_recommendedproducts(product_ID)
        return {"product": product,"recommendation":recommendedproduct}
