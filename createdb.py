import psycopg2
conn = psycopg2.connect(database="unbxd",user="postgres",password="12345",host="localhost",port="5432")
cursor=conn.cursor()

try:
    cursor.execute("drop table product")
    conn.commit()
except Exception as e:
    print(e)
try:
    cursor.execute("drop table catlevel1")
    conn.commit()
except Exception as e:
    print(e)
try:
    cursor.execute("drop table catlevel2")
    conn.commit()
except Exception as e:
    print(e)
a="create table product(uniqueId text primary key,title text,productimage text,name text,price text,availability text,productDescription text);"
b="create table catlevel1(catlevel1 text,sid SERIAL)"
c="create table catlevel2(catlevel2 text,uniqueid2 text,pid int)"
cursor.execute(a)
conn.commit()
cursor.execute(b)
conn.commit()
cursor.execute(c)
conn.commit()
conn.close()