'''
- declaration of database objects
'''

import psycopg2


class PostgresDB:

    def __init__(self):
        self.conn = psycopg2.connect(
            database="unbxd", user="postgres", password="12345", host="database", port=5432)
        self.cursor = self.conn.cursor()

    # create database tables if it does not exist
    def create_database(self):
        self.cursor.execute('''
            create table if not exists category_table(
                id serial,
                category text,
                parent_id int)
        ''')
        self.cursor.execute('''
            create table if not exists productinfo(
                product_ID text,
                product_title text,
                product_image text,
                product_name text,
                product_price text,
                product_availability text,
                product_description text,
                catid int);
            ''')
        print("Created database...")
        self.conn.commit()

    # close the database connection
    def close_database(self):
        self.conn.commit()
        self.conn.close()
        print("Connection closed.")

    # perform the operation specified by the user using the given parameters
    def operation(self, operation, params=None, res=None):
        if params != None:
            self.cursor.execute(operation, params)
            self.conn.commit()
        else:
            self.cursor.execute(operation)
        if res == 1:
            result = self.cursor.fetchall()
            return result
