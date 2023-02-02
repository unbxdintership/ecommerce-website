import psycopg2

class DB_Initialise:

    def __init__(self):
        self.conn = psycopg2.connect(database="unbxd", user="postgres",
                        password="12345", host="database", port=5432)
        self.cursor = self.conn.cursor()

    def create_database(self):
        self.cursor.execute('''
            create table category_table(
                id serial,
                category text,
                parent_id int,
                productid text,
                level int);
        ''')
        self.cursor.execute('''
            create table productinfo(product_ID text
            ,product_title text,
            product_image text,
            product_name text,
            product_price text,
            product_availability text,
            product_description text);
        ''')
        self.conn.commit()

    def close_database(self):
        self.conn.close()
        print("Connection closed.")

# dbClient = DB_Initialise()
# dbClient.create_database()
# dbClient.close_database()