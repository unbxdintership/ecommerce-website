'''
- receive the required information from the controller
- perform the required operation
- return the calculated result back to the controller
'''

import pandas as pd
from DAO.db_object import PostgresDB
from Service.db_queries import get_all_prdinfo, get_name_prdid
from Service.recommendations import Recommendation


class ProductDetailsService:

    def __init__(self):
        self.dboperator = PostgresDB()
        self.recommend = Recommendation()

    # get the details of the product, given the product ID
    def get_product(self, product_ID):
        response = self.dboperator.operation(
            get_all_prdinfo, (product_ID, ), res=1)
        result = response[0]
        return [
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5],
            result[6]
        ]

    def get_recommended_products(self, product_ID):
        try:
            recommend_productid = self.recommend.get_recommend_cosine(
                product_ID)
        except:
            name = self.dboperator.operation(
                get_name_prdid, (product_ID,), res=1)
            name = name[0][0]
            name = name.lower()
            recommend_productid = self.recommend.get_similar(name)
        recommendproducts = []
        for i in range(len(recommend_productid)):
            response = self.dboperator.operation(
                get_all_prdinfo, (recommend_productid[i],), res=1)
            result = response[0]
            recommendproducts.append(
                [result[0], result[1], result[2], result[3], result[4]])
        return recommendproducts