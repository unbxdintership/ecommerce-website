import psycopg2
conn = psycopg2.connect(database="unbxd",user="postgres",password="12345",host="localhost",port="5432")
cursor=conn.cursor()
def retrievedetails(productid):
    return 1
def insertdatabase(uniqueId,title,price,productDescription,productImage,availability,name,catlevel1Name,catlevel2Name):
    productDescription=productDescription.replace("'","`")
    title=title.replace("'","`")
    name=name.replace("'","`")
    a="insert into product values('"+uniqueId+"','"+title+"','"+productImage+"','"+name+"','"+str(price)+"','"+availability+"','"+productDescription+"')"
    cursor.execute(a)
    conn.commit()
    b="select sid from catlevel1 where catlevel1='"+catlevel1Name+"'"
    cursor.execute(b)
    result=cursor.fetchone()
    if result==None:
        cursor.execute("insert into catlevel1 values('"+catlevel1Name+"')")
        conn.commit()
        cursor.execute("select sid from catlevel1 where catlevel1='"+catlevel1Name+"'")
        result=cursor.fetchone()
    c="insert into catlevel2 values('"+catlevel2Name+"','"+uniqueId+"',"+str(result[0])+")"
    cursor.execute(c)
    conn.commit()
    
    return 1
def updatedatabase(keys,values):

    return 1