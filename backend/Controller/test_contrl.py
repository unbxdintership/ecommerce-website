from flask_restful import Resource
class Testing(Resource):
    def get(self):
        return {"hello":"Data hit successfull"}