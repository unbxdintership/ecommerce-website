from DAO.db_object import PostgresDB


class ProductDetailsService:

    def __init__(self):
        self.dboperator = PostgresDB()
        self.dboperator.create_database()

    def get_product(self, product_ID):
        self.dboperator.cursor.execute(
            "select * from productinfo where product_ID=%s", (product_ID,))
        result = self.dboperator.cursor.fetchone()
        return [
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5],
            result[6]
        ]
