from DAO.db_object import PostgresDB
from Service.misc_service import MiscService


class IngestService:

    def __init__(self):
        self.dboperator = PostgresDB()
        self.dboperator.create_database()
        self.misc = MiscService()

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
            self.dboperator.cursor.execute('''
                insert into productinfo values(%s,%s,%s,%s,%s,%s,%s)''', (
                product_ID.strip(),
                product_title.strip(),
                str(product_image).strip(),
                product_name.strip(),
                (str(product_price)).strip(),
                product_availability.strip(),
                product_description.strip(),))
            self.dboperator.conn.commit()
            if (self.misc.check_parent(product_catlevel1)):
                self.dboperator.cursor.execute(
                    '''insert into category_table (category,parent_id,level) values(%s,%s,%s)''', (product_catlevel1.strip(), 0, 1,))
                self.dboperator.conn.commit()

            self.dboperator.cursor.execute(
                '''select id from category_table where category=%s''', (product_catlevel1.strip(),))
            result = self.dboperator.cursor.fetchone()

            self.dboperator.cursor.execute('''insert into category_table (category,parent_id,productid,level) values(%s,%s,%s,%s)''', (
                product_catlevel2.strip(), result[0], product_ID, 2,))
            self.dboperator.conn.commit()
            return 1

    def verify_product(self, product_ID):
        self.dboperator.cursor.execute('''
            select * from productinfo where product_ID=%s''', (
            product_ID.strip(),))
        result = self.dboperator.cursor.fetchone()
        if result:
            return 1
        return 0

    def update_title(self, product_ID, product_title):
        self.dboperator.cursor.execute("update productinfo set product_title=%s where product_ID=%s", (
            product_title.strip(),
            product_ID.strip(),))
        self.dboperator.conn.commit()
        return 1

    def update_price(self, product_ID, product_price):
        self.dboperator.cursor.execute("update productinfo set product_price=%s where product_ID=%s", (
            (str(product_price)).strip(),
            product_ID.strip(),))
        self.dboperator.conn.commit()
        return 1

    def update_description(self, product_ID, product_description):
        self.dboperator.cursor.execute('''
            update productinfo set product_description=%s where product_ID=%s''', (
            product_description.strip(),
            product_ID.strip(),))
        self.dboperator.conn.commit()
        return 1

    def update_image(self, product_ID, product_image):
        self.dboperator.cursor.execute('''
            update productinfo set product_image=%s where product_ID=%s''', (
            product_image.strip(),
            product_ID.strip(),))
        self.dboperator.conn.commit()
        return 1

    def update_availability(self, product_ID, product_availability):
        self.dboperator.cursor.execute('''
            update productinfo set product_availability=%s where product_ID=%s''', (
            product_availability.strip(),
            product_ID.strip(),))
        self.dboperator.conn.commit()
        return 1

    def update_name(self, product_ID, product_name):
        self.dboperator.cursor.execute('''
            update productinfo set product_name=%s where product_ID=%s''', (
            product_name.strip(),
            product_ID.strip(),))
        self.dboperator.conn.commit()
        return 1
