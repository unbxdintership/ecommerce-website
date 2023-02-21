'''
- receive the required information from the controller
- perform the required operation
- return the calculated result back to the controller
'''

from DAO.db_object import PostgresDB
from Service.db_queries import get_all_cat
from Service.db_queries import get_cat_pid_cat


class MiscService:

    def __init__(self):
        self.dboperator = PostgresDB()

    # check if number of whitespaces is equal to length of the word
    def check_whitespace(self, word):
        whitespaces = 0
        for character in word:
            if character == ' ':
                whitespaces += 1
        if whitespaces == len(word):
            return 1
        else:
            return 0

    # check if a category has a parent ID
    def check_parent(self, category):
        result = self.dboperator.operation(get_all_cat, (category, ), res=1)
        if len(result) == 0:
            return 1
        return 0

    def check_catparent(self, category, parent_id):
        result = self.dboperator.operation(
            get_cat_pid_cat, (category, parent_id,), res=1)
        if len(result) == 0:
            return 1
        return 0
    # get the start and end index based on the page number

    def get_start_end(self, products_length, page):
        pages = products_length//18
        if (products_length % 18) != 0:
            pages += 1
        start, end = (page-1)*18, (page-1)*18+18
        if end >= products_length:
            end = products_length
        return [pages, start, end]
