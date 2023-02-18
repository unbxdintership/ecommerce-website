'''
- handles the incoming request
- passes the reuired information about the request to the service
- gets the response from the service
- encodes the response
- returns response to user
'''

from flask_restful import Resource, request
from Service.products_service import ProductsService
from Service.misc_service import MiscService


class ProductsCntrl(Resource):
    def __init__(self):
        self.operator = ProductsService()
        self.misc = MiscService()

    def get(self):
        # get the reuired page parameter from request
        page = int(request.args.get("page"))

        # get all the products present in the database in the ascending order
        all_products = self.operator.get_all_products()

        # get the products which need to be displayed to the user on that particular page
        result = self.misc.get_start_end(len(all_products), page)
        pages, start, end = result[0], result[1], result[2]
        products = all_products[start: end]

        return {"products": products, "pages": pages, "page": page}
