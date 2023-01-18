from flask import  Flask,request
from flask_restful import  Api,Resource
from databaseobject import *


app=Flask(__name__)
api=Api(app)

class productdetails(Resource):
    def get(self,productid):
        a=retrievedetails(productid)
        return a
api.add_resource(productdetails,"/productdetails/<string:productid>")

class ingestion(Resource):
    def post(self):
        data=request.json
        
        for i in data:
            uniqueId=i['uniqueId']
            title=i['title']
            price=i['price']
            # if 'productDescription' in i.keys()
            try:
                productDescription=i['productDescription']
            except:
                productDescription=""
            productImage=i['productImage']
            availability=i['availability']
            name=i['name']
            catlevel1Name=i['catlevel1Name']
            # i.get('catlevel2Name','')
            try:
                catlevel2Name=i['catlevel2Name']
            except:
                catlevel2Name=""
            a=insertdatabase(uniqueId,title,price,productDescription,productImage,availability,name,catlevel1Name,catlevel2Name)
        if a:
            return {"Data":"ingestion successfull"}
        else:
            return {"Data":"ingestion successfull"}
    def put(self):
        data=request.json
        for i in data:
            if i.get("uniqueId")==None:
                print("No product Id")
                break
            else:
                uniqueId=i.get("uniqueId")
            ver=verify(uniqueId)
            if ver:
                print("no unique Id present in the database")
                break
            if i.get("title")!=None:
                print("title update")
                updatetitle(uniqueId,i.get("title"))
            if i.get("price")!=None:
                print("price update")
                updateprice(uniqueId,str(i.get("price")))
            if i.get("productDescription")!=None:
                print("description update")
                updateproductDescription(uniqueId,i.get("productDescription"))
            if i.get("productImage")!=None:
                print("image update")
                updateproductImage(uniqueId,i.get("productImage"))
            if i.get("availability")!=None:
                print("availability update")
                updateavailability(uniqueId,i.get("availability"))
            if i.get("name")!=None:
                print("name update")
                updatename(uniqueId,i.get("name"))
        
        return {"data":"update successfull"}
api.add_resource(ingestion,"/ingestion")

if __name__=="__main__":
    app.run(debug=True)