'''
- receive the required information from the controller
- perform the required operation
- return the calculated result back to the controller
'''

from DAO.db_object import PostgresDB
from Service.db_queries import get_all_rnd_limit_prdinfo


class HomeService:

    def __init__(self):
        self.dboperator = PostgresDB()

    # get 18 random products from the database for the home page
    def get_random_products(self, number):
        result = self.dboperator.operation(
            get_all_rnd_limit_prdinfo, (number, ), res=1)
        final = []
        for i in result:
            final.append([i[0], i[1], i[2], i[3], i[4]])
        return final
