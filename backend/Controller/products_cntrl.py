from flask_restful import Resource, request
from Service.products_service import ProductsService
from Service.misc_service import MiscService


class ProductsCntrl(Resource):
    def __init__(self):
        self.operator = ProductsService()
        self.misc = MiscService()

    def get(self):
        page = int(request.args.get("page"))
        all_products = self.operator.get_all_products()
        result = self.misc.get_start_end(len(all_products), page)
        pages, start, end = result[0], result[1], result[2]
        products = all_products[start: end]
        return {"products": products, "pages": pages, "page": page}
