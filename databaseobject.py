import psycopg2
conn = psycopg2.connect(database="unbxd",user="postgres",password="12345",host="localhost",port="5432")
cursor=conn.cursor()
def retrievedetails(productid):
    cursor.execute("select * from product where uniqueId=%s",(productid,))
    result=cursor.fetchone()
    return {
        "uniqueId":result[0],
        "title":result[1],
        "productImage":result[2],
        "name":result[3],
        "price":result[4],
        "availability":result[5],
        "productDescription":result[6]
    }
def insertdatabase(uniqueId,title,price,productDescription,productImage,availability,name,catlevel1Name,catlevel2Name):
    cursor.execute("insert into product values(%s,%s,%s,%s,%s,%s,%s)",(uniqueId,title,productImage,name,str(price),availability,productDescription, ))
    conn.commit()
    cursor.execute("select sid from catlevel1 where catlevel1=%s",(catlevel1Name,))
    result=cursor.fetchone()
    if result==None:
        cursor.execute("insert into catlevel1 values(%s)",(catlevel1Name,))
        conn.commit()
        cursor.execute("select sid from catlevel1 where catlevel1=%s",(catlevel1Name, ))
        result=cursor.fetchone()
    cursor.execute("insert into catlevel2 values(%s,%s,%s)",(catlevel2Name,uniqueId,str(result[0])))
    conn.commit()
    return 1
def verify(uniqueId):
    cursor.execute("select * from product where uniqueId=%s",(uniqueId, ))
    a=cursor.fetchone()
    if a==None:
        return 1
    return 0
def updatetitle(uniqueId,title):
    cursor.execute("update product set title=%s where uniqueId=%s",(title,uniqueId, ))
    conn.commit()
    return 1
def updateprice(uniqueId,price):
    cursor.execute("update product set price=%s where uniqueId=%s",(price,uniqueId, ))
    conn.commit()
    return 1
def updateproductDescription(uniqueId,productDescription):
    cursor.execute("update product set productDescription=%s where uniqueId=%s",(productDescription,uniqueId, ))
    conn.commit()
    return 1
def updateproductImage(uniqueId,productImage):
    cursor.execute("update product set productImage=%s where uniqueId=%s",(productImage,uniqueId, ))
    conn.commit()
    return 1
def updateavailability(uniqueId,availability):
    cursor.execute("update product set availability=%s where uniqueId=%s",(availability,uniqueId, ))
    conn.commit()
    return 1
def updatename(uniqueId,name):
    cursor.execute("update product set name=%s where uniqueId=%s",(name,uniqueId, ))
    conn.commit()
    return 1

def catdetails(catid):
    cursor.execute("select sid from catlevel1 where catlevel1=%s",(catid, ))
    result=cursor.fetchone()
    cursor.execute("select uniqueid2 from catlevel2 where pid=%s",(str(result[0])))
    

    result=cursor.fetchall()
    uniqueid=[]
    for i in result:
        uniqueid.append(i[0])
    print(uniqueid)
    return 1