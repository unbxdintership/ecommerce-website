import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class DB_Initialise:

    def __init__(self):
        self.database = config.get('postgres', 'DATABASE')
        self.user = config.get('postgres', 'USER')
        self.password = config.get('postgres', 'PASSWORD')
        self.host = config.get('postgres', 'HOST')
        self.port = config.getint('postgres', 'PORT')
        self.conn = psycopg2.connect(database=self.database, user=self.user,
                        password=self.password, host=self.host, port=self.port)
        self.cursor = self.conn.cursor()
        print("Created DBClient.")

    def close_database(self):
        self.conn.close()
        print("Connection closed.")

    def clear_database(self):
        try:
            self.cursor.execute("drop table product")
            self.conn.commit()
            print("Dropped table - product.")
        except Exception as e:
            pass
        try:
            self.cursor.execute("drop table catlevel1")
            self.conn.commit()
            print("Dropped table - catlvl1.")
        except Exception as e:
            pass
        try:
            self.cursor.execute("drop table catlevel2")
            self.conn.commit()
            print("Dropped table - catlvl2.")
        except Exception as e:
            pass

    def create_database(self):
        self.clear_database()
        product_table = '''
            create table product(
                product_ID text primary key,
                product_title text,
                product_image text,
                product_name text,
                product_price text,
                product_availability text,
                product_description text);'''
        catlvl1_table = '''
            create table catlevel1(
                catlevel1 text,
                sid SERIAL);'''
        catlvl2_table = '''
            create table catlevel2(
                catlevel2 text,
                product_id2 text,
                pid int);'''
        self.cursor.execute(product_table)
        self.conn.commit()
        self.cursor.execute(catlvl1_table)
        self.conn.commit()
        self.cursor.execute(catlvl2_table)
        self.conn.commit()
        print("Created database.")