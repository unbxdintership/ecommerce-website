import psycopg2
from db_initialise import DB_Initialise

class DB_Operations:

    def __init__(self):
        self.operater = DB_Initialise()

    def get_product(self, product_ID):
        self.operater.cursor.execute("select * from product where product_ID=%s",(product_ID,))
        result = self.operater.cursor.fetchone()
        return {
            "product_ID": result[0],
            "product_title": result[1],
            "product_image": result[2],
            "product_name": result[3],
            "product_price": result[4],
            "product_availability": result[5],
            "product_description": result[6]
        }

    def get_category_details(self, category_lvl1, category_lvl2):
        self.operater.cursor.execute('''
            select sid from catlevel1 where catlevel1=%s''',(
                category_lvl1,))
        result = self.operater.cursor.fetchone()

        self.operater.cursor.execute('''
            select uniqueid2 from catlevel2 where pid=%s''',(
                str(result[0]),))
        result= self.operater.cursor.fetchall()
        product_IDs = []
        final = []
        for product in result:
            product_IDs.append(product[0])
        for id in product_IDs:
            self.operater.cursor.execute("select * from product where product_ID=%s",(id,))
            result = self.operater.cursor.fetchall()
            final.append(result)
        return result

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
            from product limit 9
        ''')
        result = self.operater.cursor.fetchall()
        final = []
        for i in result:
            final.append([i[0], i[1], i[2], i[3], i[4]])
        return final