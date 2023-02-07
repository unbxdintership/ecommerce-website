from flask_restful import Resource, request
from Service.category_service import CategoryService
from Service.misc_service import MiscService


class CategoryCntrl(Resource):
    def __init__(self):
        self.operator = CategoryService()
        self.misc = MiscService()

    def get(self):
        page = int(request.args.get("page"))
        category_lvl1 = request.args.get("catlvl1")
        category_lvl2 = request.args.get("catlvl2")
        category_lvl1 = category_lvl1.replace('amp', "&")
        category_lvl1 = category_lvl1.replace('space', " ")
        category_lvl2 = category_lvl2.replace('amp', "&")
        category_lvl2 = category_lvl2.replace('space', " ")
        status = self.operator.get_redis_products(category_lvl1, category_lvl2)
        if status == 1:
            all_products = self.operator.get_category_lvl2_prods(
                category_lvl1, category_lvl2)
            status1 = self.operator.insert_redis_products(
                category_lvl1, category_lvl2, all_products)
            if status1 == 1:
                print("Inserted into redis...")
        else:
            all_products = status
        result = self.misc.get_start_end(len(all_products), page)
        pages, start, end = result[0], result[1], result[2]
        products = all_products[start: end]
        return {"products": products, "pages": pages, "page": page}
