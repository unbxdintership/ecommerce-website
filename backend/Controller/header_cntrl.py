'''
- handles the incoming request
- passes the reuired information about the request to the service
- gets the response from the service
- encodes the response
- returns response to user
'''

from flask_restful import Resource
from Service.header_service import HeaderService


class HeaderCntrl(Resource):
    def __init__(self):
        self.operator = HeaderService()

    def get(self):
        categories = self.operator.get_catlevel1()

        return {"categories": categories}
