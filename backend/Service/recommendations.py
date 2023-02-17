import pandas as pd
from flask_restful import Resource, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
class recommendation():
    def __init__(self):

        self.df = pd.read_json('Service/out.json',encoding='latin-1')
        sample_size = 3000
        self.df = self.df.sample(n=sample_size,replace=False,random_state=42)
        self.df = self.df.reset_index()
        self.df = self.df.drop('index',axis=1)
        self.df['name']=self.df['name'].str.lower()
        self.df2 = self.df.drop(['categoryType','color','productUrl','availability','size','category','productImage','sku','price','catlevel4Name','uniqueId','gender','catlevel1Name','catlevel2Name','catlevel3Name',],axis=1)
        self.df2['data']=self.df2[self.df2.columns[1:]].apply(
            lambda x: ' '.join(x.dropna().astype(str)),
            axis=1
        )
        vectorizer = CountVectorizer()
        vectorized = vectorizer.fit_transform(self.df2['data'])
        self.similarity_c = cosine_similarity(vectorized)
    def getrecommend_cosine(self,name):
        self.df_name = pd.DataFrame(self.similarity_c,columns=self.df['name'],index=self.df['name']).reset_index()
        self.df_name['uniqueId']=self.df['uniqueId']
        recommendations = pd.DataFrame(self.df_name.nlargest(5,name)['uniqueId'])
        return list(recommendations['uniqueId'])
   