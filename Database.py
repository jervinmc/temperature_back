# import mysql.connector
# from decouple import config

# class Database:
#     def __init__(self):
#         self.connection = mysql.connector.connect(
#         host=config('dbHost'),
#         user=config('dbUser'),
#         password=config('dbPassword'),
#         database=config('dbDatabase')
#         )

#         self.cur=self.connection.cursor()

#     def insert(self,queryString):
#         self.cur.execute(queryString)
#         self.connection.commit()

#     def query(self,queryString):
#         self.cur.execute(queryString)
#         # self.connection.commit()
#         return self.cur.fetchall()

# # cnx = mysql.connector.connect(user='admin', password='temperature',
# #                             host='temperature.c4jf3pboyhcx.us-east-1.rds.amazonaws.com',
# #                             database='thermal')
# # cursor=cnx.cursor()
# # s = cursor.execute("SELECT * FROM thermal")
# # print(s)
# # print(s)

# # import mysql.connector

# # mydb = mysql.connector.connect(
# #   host="temperature.c4jf3pboyhcx.us-east-1.rds.amazonaws.com",
# #   user="admin",
# #   password="temperature",
# #   database="thermal"
# # )

# # mycursor = mydb.cursor()

# # mycursor.execute("SELECT * FROM thermal")

# # myresult = mycursor.fetchall()

# # for x in myresult:
# #   print(x)

# # db = Database()
# # dbs = db.query("select * from thermal")
# # print(dbs)
# # print(Database.query("select * from thermal


import psycopg2
from decouple import config

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=config("dbHost"),
            user=config("dbUser"),
            port=config("dbPort"),
            password=config("dbPassword"),
            database=config("dbDatabase")
        )

        self.cur=self.connection.cursor()

    def insert(self,queryString):
        self.cur.execute(queryString)
        self.connection.commit()

    def query(self,queryString):
        self.cur.execute(queryString)
        self.connection.commit()
        return self.cur.fetchall()
