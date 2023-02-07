from flask_restful import Resource, request
from Service.search_service import SearchService
from Service.misc_service import MiscService


class SearchCntrl(Resource):
    def __init__(self):
        self.operator = SearchService()
        self.misc = MiscService()

    def get(self):
        page = int(request.args.get("page"))
        query = request.args.get('q')
        query = query.replace("space", " ")
        query = query.replace("amp", "&")
        order = request.args.get('order')
        params = {
            "q": query
        }
        if order == "Ascending":
            params["sort"] = "price asc"
        elif order == "Descending":
            params["sort"] = "price desc"
        all_result = self.operator.get_search_products(query, order)
        result = self.misc.get_start_end(len(all_result), page)
        pages, start, end = result[0], result[1], result[2]
        products = all_result[start: end]
        return {"products": products, "pages": pages, "page": page}
