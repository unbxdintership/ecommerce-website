from flask_restful import Resource, request
class Testing(Resource):
    def get(self):
        return {"hello":"Data hit successfull"}