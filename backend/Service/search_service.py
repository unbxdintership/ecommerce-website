import requests
from Service.ingest_service import IngestService


class SearchService:

    def __init__(self):
        self.URL = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search"
        self.ing = IngestService()

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
                # product_info = {}
                # product_info['product_ID'] = products["response"]["products"][counter].get("uniqueId", ""),
                # product_info['product_title'] = products["response"]["products"][counter].get("title", ""),
                # product_info['product_price'] = products["response"]["products"][counter].get("price", ""),
                # product_info['product_description'] = products["response"]["products"][counter].get("productDescription", ""),
                # product_info['product_image'] = products["response"]["products"][counter].get("productImage", ""),
                # product_info['product_availability'] = products["response"]["products"][counter].get("availability", ""),
                # product_info['product_name'] = products["response"]["products"][counter].get("name", ""),
                # product_info['product_catlevel1'] = products["response"]["products"][counter].get("catlevel1Name", ""),
                # product_info['product_catlevel2'] = products["response"]["products"][counter].get("catlevel2Name", "")
                # res = self.ing.insert_product(product_info)
                # print(res)
        return result