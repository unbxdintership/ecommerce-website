import pandas as pd
from difflib import get_close_matches
df = pd.read_json("out.json",encoding="latin-1")
names = list(df['name'])
uniqueId = list(df['uniqueId'])
final_names = get_close_matches('phoenix suns NBA boxer briefs',names)
ids=[]
print(type(uniqueId[final_names.index(final_names[0])]))