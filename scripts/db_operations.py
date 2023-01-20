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

    def get_category_details(self, category_ID):
        self.operater.cursor.execute('''
            select sid from catlevel1 where catlevel1=%s''',(
                category_ID,))
        result = self.get_cat.cursor.fetchone()

        self.operater.cursor.execute('''
            select uniqueid2 from catlevel2 where pid=%s''',(
                str(result[0]),))
        result= self.operater.cursor.fetchall()
        product_IDs = []
        for product in result:
            product_IDs.append(product[0])
        return 1

    def insert_product(self, 
                        product_ID, 
                        product_title,
                        product_price,
                        product_description,
                        product_image,
                        product_availability,
                        product_name,
                        product_catlevel1,
                        product_catlevel2
                    ):
        self.operator.cursor.execute('''
            insert into product values(%s,%s,%s,%s,%s,%s,%s)''',(
                product_ID,
                product_title,
                product_image,
                product_name,
                str(product_price),
                product_availability,
                product_description,))
        self.operator.conn.commit()
        self.operator.cursor.execute('''
            select sid from catlevel1 where catlevel1=%s''',(
                product_catlevel1,))
        result = self.operator.cursor.fetchone()
        if result==None:
            self.operator.cursor.execute('''
                insert into catlevel1 values(%s)''',(
                    product_catlevel1,))
            self.operator.cursor.execute('''
                select sid from catlevel1 where catlevel1=%s''',(
                    product_catlevel1,))
            result = self.operator.cursor.fetchone()
        self.operator.cursor.execute('''
            insert into catlevel2 values(%s,%s,%s)''',(
                product_catlevel2,
                product_ID,
                str(result[0]),))
        self.operator.conn.commit()
        return 1

    def verify_product(self, product_ID):
        self.operator.cursor.execute('''
            select * from product where uniqueId=%s''',(
                product_ID,))
        result = self.operator.cursor.fetchone()
        if result:
            return 1
        return 0

    def update_title(self, product_ID, product_title):
        self.operator.cursor.execute('''
            update product set title=%s where uniqueId=%s''',(
                product_title,
                product_ID,))
        self.operator.conn.commit()
        return 1

    def update_price(self, product_ID, product_price):
        self.operator.cursor.execute('''
            update product set price=%s where uniqueId=%s''',(
                product_price,
                product_ID,))
        self.operator.conn.commit()
        return 1

    def update_description(self, product_ID, product_description):
        self.operator.cursor.execute('''
            update product set productDescription=%s where uniqueId=%s''',(
                product_description,
                product_ID,))
        self.operator.conn.commit()
        return 1

    def update_image(self, product_ID, product_image):
        self.operator.cursor.execute('''
            update product set productImage=%s where uniqueId=%s''',(
                product_image,
                product_ID,))
        self.operator.conn.commit()
        return 1

    def update_availability(self, product_ID, product_availability):
        self.operator.cursor.execute('''
            update product set availability=%s where uniqueId=%s''',(
                product_availability,
                product_ID,))
        self.operator.conn.commit()
        return 1

    def update_name(self, product_ID, product_name):
        self.operator.cursor.execute('''
            update product set name=%s where uniqueId=%s''',(
                product_name,
                product_ID,))
        self.operator.conn.commit()
        return 1