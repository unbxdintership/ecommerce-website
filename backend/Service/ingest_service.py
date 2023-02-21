'''
- receive the required information from the controller
- perform the required operation
- return the calculated result back to the controller
'''

from DAO.db_object import PostgresDB
from Service.misc_service import MiscService
from Service.db_queries import *


class IngestService:

    def __init__(self):
        self.dboperator = PostgresDB()
        self.misc = MiscService()

    # insert new product into the database
    def insert_product(self, product_ID, product_title, product_price, product_description, product_image, product_availability, product_name, product_catlevel1, product_catlevel2):
        if self.verify_product(product_ID):
            return 2
        else:
            if (self.misc.check_parent(product_catlevel1.strip())):
                self.dboperator.operation(set_cat_category, (product_catlevel1.strip(), 0,))

            response = self.dboperator.operation(get_id_cat, (product_catlevel1.strip(),), res=1)
            result = response[0][0]
            if (self.misc.check_catparent(product_catlevel2.strip(),result)):
                self.dboperator.operation(set_cat_category, (product_catlevel2.strip(), result,))
            catlevel2 = self.dboperator.operation(get_sid_cat,(product_catlevel2.strip(),result,), res=1)
            self.dboperator.operation(set_all_prdinfo, (
                product_ID.strip(),
                product_title.strip(),
                str(product_image).strip(),
                product_name.strip(),
                (str(product_price)).strip(),
                product_availability.strip(),
                product_description.strip(),
                catlevel2[0][0]
            ))
            return 1

    # check if the product is present in the database
    def verify_product(self, product_ID):
        result = self.dboperator.operation(
            get_all_prdinfo, (product_ID.strip(),), res=1)
        if result:
            return 1
        return 0

    # all functions required to update the respective fields of a product
    def update_title(self, product_ID, product_title):
        self.dboperator.operation(
            update_ptitle_prdinfo, (product_title.strip(), product_ID.strip(),))
        return 1

    def update_price(self, product_ID, product_price):
        self.dboperator.operation(update_pprice_prdinfo, ((
            str(product_price)).strip(), product_ID.strip(),))
        return 1

    def update_description(self, product_ID, product_description):
        self.dboperator.operation(
            update_pdescription_prdinfo, (product_description.strip(), product_ID.strip(),))
        return 1

    def update_image(self, product_ID, product_image):
        self.dboperator.operation(
            update_pimage_prdinfo, (product_image.strip(), product_ID.strip(),))
        return 1

    def update_availability(self, product_ID, product_availability):
        self.dboperator.operation(
            update_pavailability_prdinfo, (product_availability.strip(), product_ID.strip(),))
        return 1

    def update_name(self, product_ID, product_name):
        self.dboperator.operation(
            update_pname_prdinfo, (product_name.strip(), product_ID.strip(),))
        return 1