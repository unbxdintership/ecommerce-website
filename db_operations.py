import psycopg2
from db_initialise import DB_Initialise
import requests
import configparser
config=configparser.ConfigParser()
config.read('config.ini')
class DB_Operations:

    def __init__(self):
        self.operater = DB_Initialise()

    def get_product(self, product_ID):
        self.operater.cursor.execute("select * from product where product_ID=%s",(product_ID,))
        result = self.operater.cursor.fetchone()
        return [
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5],
            result[6]
        ]
    def check_whitespace(self,word):
        whitespace=0
        for character in word:
            if character==" ":
                whitespace+=1
        if whitespace==len(word):
            return 1
        return 0

    def get_category_lvl2_prods(self, category_lvl1, category_lvl2):
        self.operater.cursor.execute('''
            select sid from catlevel1 where catlevel1=%s''',(
                category_lvl1,))
        result = self.operater.cursor.fetchone()

        self.operater.cursor.execute('''
            select product_id2 from catlevel2 where pid=%s and catlevel2=%s''',(
                str(result[0]),
                category_lvl2,))
        result= self.operater.cursor.fetchall()
        product_IDs = []
        final = []
        for product in result:
            product_IDs.append(product[0])
        for id in product_IDs:
            self.operater.cursor.execute("select product_ID,product_name,product_price,product_description,product_image from product where product_ID=%s",(id,))
            result = self.operater.cursor.fetchall()
            final.append(result[0])
        return final

    def insert_product(self, 
                    product_ID, 
                    product_title,
                    product_price,
                    product_description,
                    product_image,
                    product_availability,
                    product_name,
                    product_catlevel1,
                    product_catlevel2):
        if self.verify_product(product_ID):
            return 2
        else:
            self.operater.cursor.execute('''
                insert into product values(%s,%s,%s,%s,%s,%s,%s)''',(
                    product_ID,
                    product_title,
                    product_image,
                    product_name,
                    str(product_price),
                    product_availability,
                    product_description,))
            self.operater.conn.commit()
            self.operater.cursor.execute('''
                select sid from catlevel1 where catlevel1=%s''',(
                    product_catlevel1,))
            result = self.operater.cursor.fetchone()
            if result==None:
                self.operater.cursor.execute('''
                    insert into catlevel1 values(%s)''',(
                        product_catlevel1,))
                self.operater.cursor.execute('''
                    select sid from catlevel1 where catlevel1=%s''',(
                        product_catlevel1,))
                result = self.operater.cursor.fetchone()
            self.operater.cursor.execute('''
                insert into catlevel2 values(%s,%s,%s)''',(
                    product_catlevel2,
                    product_ID,
                    str(result[0]),))
            self.operater.conn.commit()
            return 1

    def verify_product(self, product_ID):
        self.operater.cursor.execute('''
            select * from product where product_ID=%s''',(
                product_ID,))
        result = self.operater.cursor.fetchone()
        if result:
            return 1
        return 0

    def update_title(self, product_ID, product_title):
        self.operater.cursor.execute("update product set product_title=%s where product_ID=%s",(
                product_title,
                product_ID,))
        self.operater.conn.commit()
        return 1

    def update_price(self, product_ID, product_price):
        self.operater.cursor.execute("update product set product_price=%s where product_ID=%s",(
                str(product_price),
                product_ID,))
        self.operater.conn.commit()
        return 1

    def update_description(self, product_ID, product_description):
        self.operater.cursor.execute('''
            update product set product_description=%s where product_ID=%s''',(
                product_description,
                product_ID,))
        self.operater.conn.commit()
        return 1

    def update_image(self, product_ID, product_image):
        self.operater.cursor.execute('''
            update product set product_image=%s where product_ID=%s''',(
                product_image,
                product_ID,))
        self.operater.conn.commit()
        return 1

    def update_availability(self, product_ID, product_availability):
        self.operater.cursor.execute('''
            update product set product_availability=%s where product_ID=%s''',(
                product_availability,
                product_ID,))
        self.operater.conn.commit()
        return 1

    def update_name(self, product_ID, product_name):
        self.operater.cursor.execute('''
            update product set product_name=%s where product_ID=%s''',(
                product_name,
                product_ID,))
        self.operater.conn.commit()
        return 1

    def get_random_products(self):
        self.operater.cursor.execute('''
            select product_ID, 
                product_name, 
                product_price,
                product_description,
                product_image
            from product order by random() limit 9
        ''')
        result = self.operater.cursor.fetchall()
        final = []
        for i in result:
            final.append([i[0], i[1], i[2], i[3], i[4]])
        return final

    def get_catlevel1(self):
        self.operater.cursor.execute('''select * from catlevel1''')
        result=self.operater.cursor.fetchall()
        final={}
        for i in result:
            final[i[0]]=[]
            self.operater.cursor.execute('''select catlevel2,count(*) as cnt from catlevel2 where pid=%s group by catlevel2 order by cnt desc''',(str(i[1])))
            result_1=self.operater.cursor.fetchall()
            for j in result_1:
                if not self.check_whitespace(j[0]):
                    final[i[0]].append(j[0])
            
            
        return final
            #print(final)

    def search_products(self,query):
        rows = 10
        params = {
            "q": query,
            "rows": rows
        }
        response = requests.get(config.get("search_api","URL"), params)
        products = response.json()
        num_products = len(products["response"]["products"])
        result=[]
        for counter in range(0,num_products):
            result.append([products["response"]["products"][counter]["uniqueId"],products["response"]["products"][counter]["name"],products["response"]["products"][counter]["price"],products["response"]["products"][counter]["productDescription"],products["response"]["products"][counter]["productImage"]])#,products["response"]["products"][counter]["availability"],products["response"]["products"][counter]["productDescription"],products["response"]["products"][counter]["catlevel1Name"],products["response"]["products"][counter]["catlevel2Name"]])
            if self.verify_product(products["response"]["products"][counter]["uniqueId"])==0:
                self.insert_product(
                    products["response"]["products"][counter]["uniqueId"],products["response"]["products"][counter]["title"],products["response"]["products"][counter]["price"],products["response"]["products"][counter]["productDescription"],products["response"]["products"][counter]["productImage"],products["response"]["products"][counter]["availability"],products["response"]["products"][counter]["name"],products["response"]["products"][counter]["catlevel1Name"],products["response"]["products"][counter]["catlevel2Name"]
                )
        print(result)
        return result
        # result = {
        #     "product_ID": [],
        #     "product_title": [],
        #     "product_image": [],
        #     "product_name": [],
        #     "product_price": [],
        #     "product_availability": [],
        #     "product_description": [],
        #     "catlevel1": [],
        #     "catlevel2": []
        # }
        # for counter in range(0, num_products):
        #     result["product_ID"].append(products["response"]["products"][counter]["product_ID"]) 
        #     result["product_title"].append(products["response"]["products"][counter]["product_title"])
        #     result["product_image"].append(products["response"]["products"][counter]["product_image"])
        #     result["product_name"].append(products["response"]["products"][counter]["product_name"])
        #     result["product_price"].append(products["response"]["products"][counter]["product_price"])
        #     result["product_availability"].append(products["response"]["products"][counter]["product_availability"])
        #     result["product_description"].append(products["response"]["products"][counter]["product_description"])
        #     result["catlevel1"].append(products["response"]["products"][counter]["catlevel1"])
        #     result["catlevel2"].append(products["response"]["products"][counter]["catlevel2"])

        #     if self.operator.verify_product(result["product_ID"][counter]):
        #         self.operator.insert_product(
        #             result["product_ID"][counter],
        #             result["product_title"][counter],
        #             result["product_price"][counter],
        #             result["product_description"][counter],
        #             result["product_image"][counter],
        #             result["product_availability"][counter],
        #             result["product_name"][counter],
        #             result["catlevel1"][counter],
        #             result["catlevel2"][counter]
        #         )
        
        
        # return 1