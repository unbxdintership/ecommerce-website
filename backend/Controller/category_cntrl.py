'''
- handles the incoming request
- passes the reuired information about the request to the service
- gets the response from the service
- encodes the response
- returns response to user
'''

from flask_restful import Resource, request
from Service.category_service import CategoryService
from Service.misc_service import MiscService


class CategoryCntrl(Resource):
    def __init__(self):
        self.operator = CategoryService()
        self.misc = MiscService()

    def get(self, catid):
        # get the required parameters from the request
        page = int(request.args.get("page"))
        order = request.args.get("order", "None")
        
        response = self.operator.get_category_prods(catid, order)

        all_products = response['products']
        title = response['title']

        # get the products to show to the user on a particular page
        result = self.misc.get_start_end(len(all_products), page)
        pages, start, end = result[0], result[1], result[2]
        products = all_products[start: end]

        return {"products": products, "pages": pages, "page": page, "title": title}
