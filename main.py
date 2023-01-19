from flask import  Flask,request
from flask_restful import  Api,Resource
from databaseobject import *
import requests

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

class search(Resource):
    def get(self,query):
        rows=25
        params={
            "q":query,
            "rows":rows,
            
        }
        URL="https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search"
        response=requests.get(URL,params)
        data=response.json()
        length=len(data["response"]["products"])
        ret=[]
        result={"uniqueId":[],"title":[],"productImage":[],"name":[],"price":[],"availability":[],"productDescription":[],"catlevel1Name":[],"catlevel2Name":[]}
        print(ret)
        for i in range(0,length):
            
            result["uniqueId"].append(data["response"]["products"][i]["uniqueId"])
            result["title"].append(data["response"]["products"][i]["title"])
            result["productImage"].append(data["response"]["products"][i]["productImage"])
            result["name"].append(data["response"]["products"][i]["name"])
            result["price"].append(data["response"]["products"][i]["price"])
            result["availability"].append(data["response"]["products"][i]["availability"])
            result["productDescription"].append(data["response"]["products"][i]["productDescription"])
            result["catlevel1Name"].append(data["response"]["products"][i]["catlevel1Name"])
            result["catlevel2Name"].append(data["response"]["products"][i]["catlevel2Name"])    
        return result
api.add_resource(search,'/search/<string:query>')

class asort(Resource):
    def get(self,query):
        rows=25
        params={
            "q":query,
            "rows":rows,
            "sort":"price asc"
        }
        URL="https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search"
        response=requests.get(URL,params)
        data=response.json()
        length=len(data["response"]["products"])
        result={"uniqueId":[],"title":[],"productImage":[],"name":[],"price":[],"availability":[],"productDescription":[],"catlevel1Name":[],"catlevel2Name":[]}
        for i in range(0,length):
            
            result["uniqueId"].append(data["response"]["products"][i]["uniqueId"])
            result["title"].append(data["response"]["products"][i]["title"])
            result["productImage"].append(data["response"]["products"][i]["productImage"])
            result["name"].append(data["response"]["products"][i]["name"])
            result["price"].append(data["response"]["products"][i]["price"])
            result["availability"].append(data["response"]["products"][i]["availability"])
            result["productDescription"].append(data["response"]["products"][i]["productDescription"])
            result["catlevel1Name"].append(data["response"]["products"][i]["catlevel1Name"])
            result["catlevel2Name"].append(data["response"]["products"][i]["catlevel2Name"])        
        return result
api.add_resource(asort,'/asort/<string:query>')

class dsort(Resource):
    def get(self,query):
        rows=25
        params={
            "q":query,
            "rows":rows,
            "sort":"price desc"
        }
        URL="https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search"
        response=requests.get(URL,params)
        data=response.json()
        length=len(data["response"]["products"])
        result={"uniqueId":[],"title":[],"productImage":[],"name":[],"price":[],"availability":[],"productDescription":[],"catlevel1Name":[],"catlevel2Name":[]}
        for i in range(0,length):
            
            result["uniqueId"].append(data["response"]["products"][i]["uniqueId"])
            result["title"].append(data["response"]["products"][i]["title"])
            result["productImage"].append(data["response"]["products"][i]["productImage"])
            result["name"].append(data["response"]["products"][i]["name"])
            result["price"].append(data["response"]["products"][i]["price"])
            result["availability"].append(data["response"]["products"][i]["availability"])
            result["productDescription"].append(data["response"]["products"][i]["productDescription"])
            result["catlevel1Name"].append(data["response"]["products"][i]["catlevel1Name"])
            result["catlevel2Name"].append(data["response"]["products"][i]["catlevel2Name"])        
        return result
api.add_resource(dsort,'/dsort/<string:query>')

class category(Resource):
    def get(self,catid):
        catdetails(catid)
        return 1
api.add_resource(category,'/category/<string:catid>')
if __name__=="__main__":
    app.run(debug=True)