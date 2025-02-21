from utils.query import query
import re
import sys
import pandas as pd
sys.path.append("model")

def getAlladlist():
    adlist=query('select * from artwork_duplicates',[],'select')
    return adlist
def getAllaflist():
    aflist=query('select * from artwork_filled',[],'select')
    return aflist
def getAllHotWords():
    data=[]
    df=pd.read_csv('./model/artwork_typecount.csv',encoding='utf-8')
    for i in df.values:
        try:
            data.append([
                re.search('[\u4e00-\u9fa5]+',str(i)).group(),
                re.search('\d+',str(i)).group(),
            ])
        except:
            continue
    return data

if __name__ == '__main__':
    print(getAllHotWords())

