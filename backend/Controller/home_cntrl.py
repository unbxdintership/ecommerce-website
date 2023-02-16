'''
- handles the incoming request
- passes the reuired information about the request to the service
- gets the response from the service
- encodes the response
- returns response to user
'''

from flask_restful import Resource
from Service.home_service import HomeService


class HomeCntrl(Resource):
    def __init__(self):
        self.operator = HomeService()

    def get(self):
        # get 18 random products to be displayed as featured products on home page
        products = self.operator.get_random_products(18)

        return {"products": products}
