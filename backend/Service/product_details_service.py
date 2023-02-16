'''
- receive the required information from the controller
- perform the required operation
- return the calculated result back to the controller
'''

from DAO.db_object import PostgresDB
from Service.db_queries import get_all_prdinfo


class ProductDetailsService:

    def __init__(self):
        self.dboperator = PostgresDB()

    # get the details of the product, given the product ID
    def get_product(self, product_ID):
        response = self.dboperator.operation(get_all_prdinfo, (product_ID, ), res=1)
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