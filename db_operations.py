import requests
from db_initialise import DB_Initialise
from configparser import ConfigParser
import redis

config = ConfigParser()
config.read('config.ini')


class DB_Operations:

    def __init__(self):
        self.operater = DB_Initialise()
        self.r = redis.Redis(host='redis', port=6378)

    def check_whitespace(self, word):
        whitespaces = 0
        for character in word:
            if character == ' ':
                whitespaces += 1
        if whitespaces == len(word):
            return 1
        else:
            return 0

    def insert_redis_products(self, catlvl1, catlvl2, products):
        redis_query = f"{catlvl1.strip()}-{catlvl2.strip()}"
        # self.r.psetex(redis_query, 100000, products)
        for product in products:
            self.r.rpush(redis_query, *product)
        self.r.expire(redis_query, 60)
        return 1

    def get_redis_products(self, catlvl1, catlvl2):
        redis_query = f"{catlvl1.strip()}-{catlvl2.strip()}"
        final = []
        if self.r.exists(redis_query):
            products = self.r.lrange(redis_query, 0, -1)
            for length in range(len(products)//5):
                product = products[length*5: length*5+5]
                for index in range(len(product)):
                    product[index] = product[index].decode()
                final.append(product)
            print("Got products from redis...")
            return final
        else:
            return 1

    def get_product(self, product_ID):
        self.operater.cursor.execute(
            "select * from productinfo where product_ID=%s", (product_ID,))
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
    # to change-done

    def get_category_lvl2_prods(self, category_lvl1, category_lvl2):
        self.operater.cursor.execute('''
            select id from category_table where category=%s''', (
            category_lvl1,))
        result = self.operater.cursor.fetchone()

        self.operater.cursor.execute('''
            select productid from category_table where parent_id=%s and category=%s''', (
            result[0],
            category_lvl2,))
        result = self.operater.cursor.fetchall()
        product_IDs = []
        final = []
        for product in result:
            product_IDs.append(product[0])
        for id in product_IDs:
            self.operater.cursor.execute('''
                select product_ID,
                        product_name,
                        product_price,
                        product_description,
                        product_image 
                    from productinfo where product_ID=%s''', (id,))
            result = self.operater.cursor.fetchone()
            final.append(result)
        return final
    # to change-done

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
                insert into productinfo values(%s,%s,%s,%s,%s,%s,%s)''', (
                product_ID.strip(),
                product_title.strip(),
                str(product_image).strip(),
                product_name.strip(),
                (str(product_price)).strip(),
                product_availability.strip(),
                product_description.strip(),))
            self.operater.conn.commit()
            if (self.checkparent(product_catlevel1)):
                self.operater.cursor.execute(
                    '''insert into category_table (category,parent_id,level) values(%s,%s,%s)''', (product_catlevel1.strip(), 0, 1,))
                self.operater.conn.commit()
            # insert catlevel 2

            self.operater.cursor.execute(
                '''select id from category_table where category=%s''', (product_catlevel1.strip(),))
            result = self.operater.cursor.fetchone()

            self.operater.cursor.execute('''insert into category_table (category,parent_id,productid,level) values(%s,%s,%s,%s)''', (
                product_catlevel2.strip(), result[0], product_ID, 2,))
            self.operater.conn.commit()
            return 1

    def checkparent(self, category):
        self.operater.cursor.execute(
            '''select * from category_table where category=%s''', (category,))
        result = self.operater.cursor.fetchone()
        if result == None:
            return 1
        return 0

    def verify_product(self, product_ID):
        self.operater.cursor.execute('''
            select * from productinfo where product_ID=%s''', (
            product_ID.strip(),))
        result = self.operater.cursor.fetchone()
        if result:
            return 1
        return 0

    def update_title(self, product_ID, product_title):
        self.operater.cursor.execute("update productinfo set product_title=%s where product_ID=%s", (
            product_title.strip(),
            product_ID.strip(),))
        self.operater.conn.commit()
        return 1

    def update_price(self, product_ID, product_price):
        self.operater.cursor.execute("update productinfo set product_price=%s where product_ID=%s", (
            (str(product_price)).strip(),
            product_ID.strip(),))
        self.operater.conn.commit()
        return 1

    def update_description(self, product_ID, product_description):
        self.operater.cursor.execute('''
            update productinfo set product_description=%s where product_ID=%s''', (
            product_description.strip(),
            product_ID.strip(),))
        self.operater.conn.commit()
        return 1

    def update_image(self, product_ID, product_image):
        self.operater.cursor.execute('''
            update productinfo set product_image=%s where product_ID=%s''', (
            product_image.strip(),
            product_ID.strip(),))
        self.operater.conn.commit()
        return 1

    def update_availability(self, product_ID, product_availability):
        self.operater.cursor.execute('''
            update productinfo set product_availability=%s where product_ID=%s''', (
            product_availability.strip(),
            product_ID.strip(),))
        self.operater.conn.commit()
        return 1

    def update_name(self, product_ID, product_name):
        self.operater.cursor.execute('''
            update productinfo set product_name=%s where product_ID=%s''', (
            product_name.strip(),
            product_ID.strip(),))
        self.operater.conn.commit()
        return 1

    def get_random_products(self):
        self.operater.cursor.execute('''
            select product_ID, 
                product_name, 
                product_price,
                product_description,
                product_image
            from productinfo order by random()
        ''')
        result = self.operater.cursor.fetchall()
        final = []
        for i in result:
            final.append([i[0], i[1], i[2], i[3], i[4]])
        return final
    # to change

    def get_catlevel1(self):
        self.operater.cursor.execute('''
            select category, id from category_table where level=%s
        ''', (1,))
        result = self.operater.cursor.fetchall()
        # print("result"result)

        final = {}
        for i in result:
            final[i[0]] = []
            # print(type(i[1]))
            self.operater.cursor.execute(''' 
                select distinct category
                from category_table where parent_id=%s
            ''', (i[1],))
            result_1 = self.operater.cursor.fetchall()
            for j in result_1:
                if not self.check_whitespace(j[0]):
                    final[i[0]].append(j[0])
        return final

    def get_search_products(self, query, order=None):
        rows = 90
        params = {
            "rows": rows,
            "q": query,
        }
        if order == 'Ascending':
            params["sort"] = "price asc"
        elif order == 'Descending':
            params['sort'] = "price desc"
        response = requests.get(config.get("search_api", "URL"), params)
        products = response.json()
        num_products = len(products["response"]["products"])
        result = []
        for counter in range(0, num_products):
            result.append([
                products["response"]["products"][counter].get("uniqueId", ""),
                products["response"]["products"][counter].get("name", ""),
                products["response"]["products"][counter].get("price", ""),
                products["response"]["products"][counter].get(
                    "productDescription", ""),
                products["response"]["products"][counter].get(
                    "productImage", "")
            ])

            if self.verify_product(products["response"]["products"][counter]["uniqueId"]) == 0:
                self.insert_product(
                    products["response"]["products"][counter].get(
                        "uniqueId", ""),
                    products["response"]["products"][counter].get("title", ""),
                    products["response"]["products"][counter].get("price", ""),
                    products["response"]["products"][counter].get(
                        "productDescription", ""),
                    products["response"]["products"][counter].get(
                        "productImage", ""),
                    products["response"]["products"][counter].get(
                        "availability", ""),
                    products["response"]["products"][counter].get("name", ""),
                    products["response"]["products"][counter].get(
                        "catlevel1Name", ""),
                    products["response"]["products"][counter].get(
                        "catlevel2Name", "")
                )

        return result
