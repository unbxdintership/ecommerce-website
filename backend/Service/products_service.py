'''
- receive the required information from the controller
- perform the required operation
- return the calculated result back to the controller
'''

from DAO.db_object import PostgresDB
from Service.db_queries import *


class ProductsService:
    def __init__(self):
        self.dboperator = PostgresDB()

    # get all the products present in the database in the ascending order
    def get_all_products(self):
        result = self.dboperator.operation(get_fields_order_prdinfo, res=1)
        final = []
        for i in result:
            final.append([i[0], i[1], i[2], i[3], i[4]])
        return final
