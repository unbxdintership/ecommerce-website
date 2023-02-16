'''
- receive the required information from the controller
- perform the required operation
- return the calculated result back to the controller
'''

import requests
from Service.ingest_service import IngestService


class SearchService:

    def __init__(self):
        self.URL = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search"
        self.ing = IngestService()

    # given a query, get the products from the Unbxd Search API
    def get_search_products(self, query, order=None):
        rows = 90
        params = {
            "rows": rows,
            "q": query,
        }
        if order == 'Ascending':
            params["sort"] = "price asc"
        elif order == 'Descending':
            params['sort'] = "price desc"

        response = requests.get(self.URL, params)
        products = response.json()
        num_products = len(products["response"]["products"])
        result = []
        for counter in range(0, num_products):
            result.append([
                products["response"]["products"][counter].get("uniqueId", ""),
                products["response"]["products"][counter].get("name", ""),
                products["response"]["products"][counter].get("price", ""),
                products["response"]["products"][counter].get(
                    "productDescription", ""),
                products["response"]["products"][counter].get(
                    "productImage", "")
            ])

            if self.ing.verify_product(products["response"]["products"][counter]["uniqueId"]) == 0:
                self.ing.insert_product(
                    products["response"]["products"][counter].get(
                        "uniqueId", ""),
                    products["response"]["products"][counter].get("title", ""),
                    products["response"]["products"][counter].get("price", ""),
                    products["response"]["products"][counter].get(
                        "productDescription", ""),
                    products["response"]["products"][counter].get(
                        "productImage", ""),
                    products["response"]["products"][counter].get(
                        "availability", ""),
                    products["response"]["products"][counter].get("name", ""),
                    products["response"]["products"][counter].get(
                        "catlevel1Name", ""),
                    products["response"]["products"][counter].get(
                        "catlevel2Name", "")
                )
        return result
