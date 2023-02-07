from flask_restful import Resource
from Service.home_service import HomeService


class HomeCntrl(Resource):
    def __init__(self):
        self.operator = HomeService()

    def get(self):
        products = self.operator.get_random_products(18)
        return {"products": products}
