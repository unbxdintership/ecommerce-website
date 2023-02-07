from DAO.db_object import PostgresDB
from Service.misc_service import MiscService


class HeaderService:

    def __init__(self):
        self.dboperator = PostgresDB()
        self.dboperator.create_database()
        self.misc = MiscService()

    def get_catlevel1(self):
        self.dboperator.cursor.execute('''
            select category, id from category_table where level=%s
        ''', (1,))
        result = self.dboperator.cursor.fetchall()

        final = {}
        for i in result:
            final[i[0]] = []
            self.dboperator.cursor.execute(''' 
                select distinct category
                from category_table where parent_id=%s
            ''', (i[1],))
            result_1 = self.dboperator.cursor.fetchall()
            for j in result_1:
                if not self.misc.check_whitespace(j[0]):
                    final[i[0]].append(j[0])
        return final