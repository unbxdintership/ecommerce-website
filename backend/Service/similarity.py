from difflib import get_close_matches
import pandas as pd
df=pd.read_json("out.json",encoding="latin-1")
df['name']=df['name'].str.lower()
df['productDescription'] = df['productDescription'].str.lower()
df = df.astype({'productDescription':str,"catlevel1Name":str})
# df  = df.astype()
#name = list(df['name'])
#name=list(df['name']+df['productDescription'])
name = list(df['name']+df['catlevel1Name'])
print(get_close_matches('two row knot pearl drop y-necklace',name))
#print(name)