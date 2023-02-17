# from DAO.db_object import PostgresDB
# from Service.db_queries import get_all_prdinfo
# from Service.db_queries import get_name_prdid
# from Service.recommendations import Recommendation

# class ProductDetailsService:

#     def __init__(self):
#         self.dboperator = PostgresDB()
#         self.recommend =  Recommendation()
#     def get_product(self, product_ID):
#         response = self.dboperator.operation(get_all_prdinfo, (product_ID, ), res=1)
#         result = response[0]
#         return [
#             result[0],
#             result[1],
#             result[2],
#             result[3],
#             result[4],
#             result[5],
#             result[6]
#         ]
from DAO.db_object import PostgresDB
from Service.db_queries import get_all_prdinfo
from Service.db_queries import get_name_prdid
from Service.recommendations import recommendation
class ProductDetailsService:

    def __init__(self):
        self.dboperator = PostgresDB()
        self.recommend =  recommendation()
    def get_product(self, product_ID):
        # self.dboperator.cursor.execute(
        #     "select * from productinfo where product_ID=%s", (product_ID,))
        # result = self.dboperator.cursor.fetchone()
        response = self.dboperator.operation(get_all_prdinfo, (product_ID, ), res=1)
        result = response[0]
        return [
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5],
            result[6]
        ]
    def get_recommendedproducts(self,product_ID):
        name = self.dboperator.operation(get_name_prdid,(product_ID, ),res=1)
        
        recommend_productid = self.recommend.getrecommend_cosine(name[0][0])
        recommendproducts=[]
        for i in range(len(recommend_productid)):
            if recommend_productid[i]!=product_ID:
                k=self.dboperator.operation(get_all_prdinfo,(recommend_productid[i],),res=1)
                recommendproducts.append([k[0][0],k[0][1],k[0][2],k[0][3],k[0][4]])
        return recommendproducts