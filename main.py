from flask import  Flask,request
from flask_restful import  Api,Resource
from databaseobject import *
app=Flask(__name__)
api=Api(app)

class productdetails(Resource):
    def get(self,productid):
        a=retrievedetails(productid)
        return a
api.add_resource(productdetails,"/category/<string:productid>")

class ingestion(Resource):
    def post(self):
        data=request.json
        
        for i in data:
            uniqueId=i['uniqueId']
            title=i['title']
            price=i['price']
            try:
                productDescription=i['productDescription']
            except:
                productDescription=""
            productImage=i['productImage']
            availability=i['availability']
            name=i['name']
            catlevel1Name=i['catlevel1Name']
            try:
                catlevel2Name=i['catlevel2Name']
            except:
                catlevel2Name=""
            a=insertdatabase(uniqueId,title,price,productDescription,productImage,availability,name,catlevel1Name,catlevel2Name)
        return {1:1}
        uniqueid=request.form['uniqueId']
        title=request.form['title']
        price=request.form['price']
        try:
            description=request.form['productDescription']
        except:
            description=""
        imageurl=request.form['productImage']
        availability=request.form['availability']
        name=request.form['name']
        catlevel1=request.form['catlevel1Name']
        try:
            catlevel2=request.form['catlevel2Name']
        except:
            catlevel2=""
        return {1:1}
        a=insertdatabase(uniqueid,title,price,description,imageurl,availability,name,catlevel1,catlevel2)
        if a:
            return {"data":"insertion successfull"}
        else:
            return {"data":"insertion failed"}
    def put(self):
        a=request.form
        b=list(a.keys())
        values=[]
        for i in b:
            values.append(request.form[i])
        
        return {1:1}
api.add_resource(ingestion,"/ingestion")

if __name__=="__main__":
    app.run(debug=True)