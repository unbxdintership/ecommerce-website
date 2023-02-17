from DAO.db_object import PostgresDB
from DAO.cache_object import RedisCache
from Service.db_queries import *


class CategoryService:
    def __init__(self):
        self.dboperator = PostgresDB()
        self.cacheoperator = RedisCache()

    def insert_redis_products(self, catlvl1, catlvl2, products):
        redis_query = f"{catlvl1.strip()}-{catlvl2.strip()}"
        for product in products:
            self.cacheoperator.redis.rpush(redis_query, *product)
        self.cacheoperator.redis.expire(redis_query, 60)
        return 1

    def get_redis_products(self, catlvl1, catlvl2):
        redis_query = f"{catlvl1.strip()}-{catlvl2.strip()}"
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

    def get_category_lvl2_prods(self, category_lvl1, category_lvl2, order=None):
        # finals = category_lvl2 + str(order)
        status = self.get_redis_products(category_lvl1, category_lvl2)
        if status == 1:
            # self.dboperator.cursor.execute('''
            #     select id from category_table where category=%s''', (
            #     category_lvl1,))
            # result = self.dboperator.cursor.fetchone()
            response = self.dboperator.operation(
                get_id_cat, (category_lvl1, ), res=1)
            result = response[0]
            # self.dboperator.cursor.execute('''
            #     select productid from category_table where parent_id=%s and category=%s''', (
            #     result[0],
            #     category_lvl2,))
            # result = self.dboperator.cursor.fetchall()
            result = self.dboperator.operation(
                get_pid_cat, (result[0], category_lvl2, ), res=1)
            product_IDs = []
            print("In category service", order)
            final = []
            for product in result:
                product_IDs.append(product[0])
            for id in product_IDs:
                response = self.dboperator.operation(
                    get_fields_prdinfo, (id,), res=1)
                result = response[0]
                # result = list(result)
                # temp = result[0]
                # result[0] = float(result[2])
                # result[2] = temp
                final.append(result)
            # final=list(final)
            # print(final)

            # result_list = []

            # if order != None:
            #     for i in final:
            #         result_list.append([float(i[2]), i[1], i[0], i[3], i[4]])
            #     if order == 'Ascending':
            #         result_list.sort()
            #     else:
            #         result_list.sort(reverse=True)
            #     print(result_list)
            #     for i in result_list:
            #         temp = i[0]
            #         i[0] = i[2]
            #         i[2] = temp
            #         i[2] = str(i[2])
            #     # print(result_list)
            # else:
            #     return final

            insert_status = self.insert_redis_products(
                category_lvl1, category_lvl2, final)
            if insert_status == 1:
                print("Inserted into redis...")

            # if order=='Ascending':
            #     final = final.sort()
            # elif order=='Descending':
            #     final = final.sort(reverse=True)
            result_list = []

            if order != 'None':
                for i in final:
                    result_list.append([float(i[2]), i[1], i[0], i[3], i[4]])
                if order == 'Ascending':
                    result_list.sort()
                else:
                    result_list.sort(reverse=True)
                for i in result_list:
                    temp = i[0]
                    i[0] = i[2]
                    i[2] = temp
                    i[2] = str(i[2])
                return result_list

            return final
        else:

            # if order=='Ascending':
            #     status = status.sort()
            # elif order=='Descending':
            #     status = status.sort(reverse=True)
            result_list = []

            if order != 'None':
                for i in status:
                    result_list.append([float(i[2]), i[1], i[0], i[3], i[4]])
                if order == 'Ascending':
                    result_list.sort()
                else:
                    result_list.sort(reverse=True)
                for i in result_list:
                    temp = i[0]
                    i[0] = i[2]
                    i[2] = temp
                    i[2] = str(i[2])
                return result_list

            return status
