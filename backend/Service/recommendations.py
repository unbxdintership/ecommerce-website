import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches


class Recommendation():
    def __init__(self):

        self.df = pd.read_json('Service/out.json', encoding='latin-1')
        sample_size = 3000
        self.df = self.df.sample(n=sample_size, replace=False, random_state=42)
        self.df = self.df.reset_index()
        self.df = self.df.drop('index', axis=1)
        self.df['name'] = self.df['name'].str.lower()
        self.df = self.df.astype({'catlevel2Name': str})
        self.df['name'] = self.df['name']+" "+self.df['catlevel2Name']
        self.df2 = self.df.drop(['categoryType', 'color', 'productUrl', 'availability', 'size', 'category', 'productImage',
                                'sku', 'price', 'catlevel4Name', 'uniqueId', 'gender', 'catlevel1Name', 'catlevel2Name', 'catlevel3Name',], axis=1)
        self.df2['data'] = self.df2[self.df2.columns[1:]].apply(
            lambda x: ' '.join(x.dropna().astype(str)),
            axis=1
        )
        vectorizer = CountVectorizer()
        vectorized = vectorizer.fit_transform(self.df2['data'])
        self.similarity_c = cosine_similarity(vectorized)
        self.df_name = pd.DataFrame(
            self.similarity_c, columns=self.df['uniqueId'], index=self.df['uniqueId']).reset_index()

    def get_recommend_cosine(self, name):
        recommendations = pd.DataFrame(
            self.df_name.nlargest(5, name)['uniqueId'])
        recommendations = recommendations[recommendations['uniqueId'] != name]
        return list(recommendations['uniqueId'])

    def get_similar(self, name):
        names = list(self.df['name'])
        ids = list(self.df['uniqueId'])
        final_names = get_close_matches(name, names)
        return self.get_recommend_cosine(ids[final_names.index(final_names[0])])
