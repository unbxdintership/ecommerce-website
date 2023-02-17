# from DAO.db_object import PostgresDB
# from Service.db_queries import get_all_rnd_limit_prdinfo


# class HomeService:

#     def __init__(self):
#         self.dboperator = PostgresDB()

#     def get_random_products(self, number):
#         # self.dboperator.cursor.execute('''
#         #     select product_ID, 
#         #         product_name, 
#         #         product_price,
#         #         product_description,
#         #         product_image
#         #     from productinfo order by random() limit %s
#         # ''', (number,))
#         # result = self.dboperator.cursor.fetchall()
#         result = self.dboperator.operation(get_all_rnd_limit_prdinfo, (number, ), res=1)
#         final = []
#         for i in result:
#             final.append([i[0], i[1], i[2], i[3], i[4]])
#         return final
from DAO.db_object import PostgresDB
from Service.db_queries import get_all_rnd_limit_prdinfo


class HomeService:

    def __init__(self):
        self.dboperator = PostgresDB()

    def get_random_products(self, number):
        # self.dboperator.cursor.execute('''
        #     select product_ID, 
        #         product_name, 
        #         product_price,
        #         product_description,
        #         product_image
        #     from productinfo order by random() limit %s
        # ''', (number,))
        # result = self.dboperator.cursor.fetchall()
        result = self.dboperator.operation(get_all_rnd_limit_prdinfo, (number, ), res=1)
        final = []
        for i in result:
            final.append([i[0], i[1], i[2], i[3], i[4]])
        return final