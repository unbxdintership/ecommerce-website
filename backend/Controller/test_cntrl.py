'''
- API to check if requests to backend actually hit the backend
'''

from flask_restful import Resource


class Testing(Resource):

    def get(self):
        return {"hello": "Data hit successfull"}
