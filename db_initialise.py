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

    def close_database(self):
        self.conn.close()
        print("Connection closed.")