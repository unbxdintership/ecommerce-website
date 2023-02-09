from DAO.db_object import PostgresDB
from Service.db_queries import get_fields_order_prdinfo


class ProductsService:

    def __init__(self):
        self.dboperator = PostgresDB()

    def get_all_products(self):
        # self.dboperator.cursor.execute('''
        #     select product_ID,
        #         product_name,
        #         product_price,
        #         product_description,
        #         product_image
        #     from productinfo order by product_name
        # ''')
        # result = self.dboperator.cursor.fetchall()
        result = self.dboperator.operation(get_fields_order_prdinfo, res=1)
        final = []
        for i in result:
            final.append([i[0], i[1], i[2], i[3], i[4]])
        return final
