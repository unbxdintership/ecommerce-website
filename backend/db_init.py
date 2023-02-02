from db_initialise import DB_Initialise

dbClient = DB_Initialise()
dbClient.create_database()
dbClient.close_database()