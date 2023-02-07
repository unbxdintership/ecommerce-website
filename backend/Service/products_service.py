from DAO.db_object import PostgresDB


class ProductsService:

    def __init__(self):
        self.dboperator = PostgresDB()
        self.dboperator.create_database()

    def get_all_products(self):
        self.dboperator.cursor.execute('''
            select product_ID,
                product_name,
                product_price,
                product_description,
                product_image
            from productinfo order by product_name
        ''')
        result = self.dboperator.cursor.fetchall()
        final = []
        for i in result:
            final.append([i[0], i[1], i[2], i[3], i[4]])
        return final
