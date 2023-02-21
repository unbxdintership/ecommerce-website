'''
- receive the required information from the controller
- perform the required operation
- return the calculated result back to the controller
'''

from DAO.db_object import PostgresDB
from DAO.cache_object import RedisCache
from Service.db_queries import *


class CategoryService:
    def __init__(self):
        self.dboperator = PostgresDB()
        self.cacheoperator = RedisCache()

    # insert into redis cache
    def insert_redis_products(self, catid, order, products):
        redis_query = f"{catid.strip()}-{order.strip()}"
        for product in products:
            self.cacheoperator.redis.rpush(redis_query, *product)
        self.cacheoperator.redis.expire(redis_query, 60)
        return 1

    # get the value from redis cache, if present
    def get_redis_products(self, catid, order):
        redis_query = f"{catid.strip()}-{order.strip()}"
        final = []
        if self.cacheoperator.redis.exists(redis_query):
            products = self.cacheoperator.redis.lrange(redis_query, 0, -1)
            for length in range(len(products)//5):
                product = products[length*5: length*5+5]
                for index in range(len(product)):
                    product[index] = product[index].decode()
                final.append(product)
            print("Got products from redis...")
            return final
        else:
            return 1

    def get_category_prods(self, catid, order):
        status = self.get_redis_products(catid, order)
        catlevel1name = ''
        catlevel2name = ''
        '''
        check if id has parentid=0 -> display catlvl1 products
        check if id has parentid!=0 -> display catlvl2 products
        '''

        if status == 1:
            response = self.dboperator.operation(get_pid_cat, (catid,), res=1)
            result = response[0]
            catlevel1name = self.dboperator.operation(
                get_par_cat_cattable, (catid,), res=1)
            if result[0] == 0 or result[0] == '0':
                all_catids = []
                response = self.dboperator.operation(
                    get_cat_id_cat, (catid,), res=1)
                for i in response:
                    all_catids.append(i[1])
                all_products = []
                for id in all_catids:
                    products = self.dboperator.operation(
                        get_fields_catid_prdinfo, (id,), res=1)
                    for product in products:
                        all_products.append(
                            [product[0], product[1], product[2], product[3], product[4]])
                # return all_products
                result_list = []
                if order != 'None':
                    for i in all_products:
                        result_list.append(
                            [float(i[2]), i[1], i[0], i[3], i[4]])
                    if order == 'Ascending':
                        result_list.sort()
                    else:
                        result_list.sort(reverse=True)
                    for i in result_list:
                        temp = i[0]
                        i[0] = i[2]
                        i[2] = temp
                        i[2] = str(i[2])
                    insert_status = self.insert_redis_products(
                        catid, order, result_list)
                    if insert_status == 1:
                        print("Inserted into redis...")
                    return {"products": result_list, "title": catlevel1name[0][0]}
                insert_status = self.insert_redis_products(
                    catid, order, all_products)
                if insert_status == 1:
                    print("Inserted into redis...")
                return {"products": all_products, "title": catlevel1name[0][0]}

            else:
                all_products = []
                products = self.dboperator.operation(
                    get_fields_catid_prdinfo, (catid,), res=1)
                catlevel2name = self.dboperator.operation(
                    get_par_cat_cattable, (catid,), res=1)
                catlevel1name = self.dboperator.operation(
                    get_par_cat_cattable, (catlevel2name[0][1],), res=1)

                for product in products:
                    all_products.append(
                        [product[0], product[1], product[2], product[3], product[4]])
                result_list = []
                if order != 'None':
                    for i in all_products:
                        result_list.append(
                            [float(i[2]), i[1], i[0], i[3], i[4]])
                    if order == 'Ascending':
                        result_list.sort()
                    else:
                        result_list.sort(reverse=True)
                    for i in result_list:
                        temp = i[0]
                        i[0] = i[2]
                        i[2] = temp
                        i[2] = str(i[2])
                    insert_status = self.insert_redis_products(
                        catid, order, result_list)
                    if insert_status == 1:
                        print("Inserted into redis...")
                    return {"products": result_list, "title": catlevel1name[0][0]+"-"+catlevel2name[0][0]}
                insert_status = self.insert_redis_products(
                    catid, order, all_products)
                if insert_status == 1:
                    print("Inserted into redis...")
                return {"products": all_products, "title": catlevel1name[0][0]+"-"+catlevel2name[0][0]}

        else:
            response = self.dboperator.operation(get_pid_cat, (catid,), res=1)
            result = response[0]
            if result[0] == '0' or result[0] == 0:
                catlevel1name = self.dboperator.operation(
                    get_par_cat_cattable, (catid,), res=1)
                return {"products": status, "title": catlevel1name[0][0]}
            else:
                catlevel2name = self.dboperator.operation(
                    get_par_cat_cattable, (catid,), res=1)
                catlevel1name = self.dboperator.operation(
                    get_par_cat_cattable, (catlevel2name[0][1],), res=1)
                return {"products": status, "title": catlevel1name[0][0]+"-"+catlevel2name[0][0]}
