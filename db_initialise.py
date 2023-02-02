import psycopg2
# import configparser

# config = configparser.ConfigParser()
# config.read('config.ini')

class DB_Initialise:

    def __init__(self):
        self.conn = psycopg2.connect(database="unbxd", user="postgres",
                        password="12345", host="postgres", port=5431)
        self.cursor = self.conn.cursor()

    def close_database(self):
        self.conn.close()
        print("Connection closed.")