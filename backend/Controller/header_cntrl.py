from flask_restful import Resource
from Service.header_service import HeaderService


class HeaderCntrl(Resource):
    def __init__(self):
        self.operator = HeaderService()

    def get(self):
        categories = self.operator.get_catlevel1()
        return {"categories": categories}
