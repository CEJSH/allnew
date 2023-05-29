import chardet
import pandas as pd
import json
from fastapi import FastAPI
import requests
import urllib.request
import datetime
import os
import numpy as np

app = FastAPI()

with open('forest_rate.csv', 'rb') as file:
    result = chardet.detect(file.read())
encoding = result['encoding']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../../secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as e:
        # print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

df = pd.read_csv('forest_rate.csv', encoding=encoding)
print(df['park_cnt'].sum())
df = df.iloc[:,[0,1,3]]
df.insert(0,'guname',[str(df.iloc[[i],[0]].values[0][0])[:5] for i in range(len(df))])
parkareaperone = {
        '강남구' : (6.51),
        '관악구' : (2.47),
        '강북구' : (6.65),
        '강동구' : (4.53),
        '강서구' : (6.17),
        '광진구' : (3.34),
        '구로구' : (3.26),
        '금천구' : (1.60),
        '노원구' : (5.57),
        '도봉구' : (3.86),
        '동대문구' : (3.29),
        '동작구' : (7.64),
        '마포구' : (11.17),
        '서초구' : (5.58),
        '성동구' : (9.42),
        '성북구' : (4.94),
        '송파구' : (6.35),
        '서대문구' : (5.15),
        '양천구' : (4.03),
        '영등포구' : (7.36),
        '용산구' : (6.77),
        '은평구' : (2.57),
        '종로구' : (18.73),
        '중구' : (10.75),
        '중랑구' : (4.23)
}
sigunguCdList = {
        '강남구' : (11680),
        '관악구' : (11620),
        '강북구' : (11305),
        '강동구' : (11740),
        '강서구' : (11500),
        '광진구' : (11215),
        '구로구' : (11530),
        '금천구' : (11545),
        '노원구' : (11350),
        '도봉구' : (11320),
        '동대문구' : (11230),
        '동작구' : (11590),
        '마포구' : (11440),
        '서초구' : (11650),
        '성동구' : (11200),
        '성북구' : (11290),
        '송파구' : (11710),
        '서대문구' : (11410),
        '양천구' : (11470),
        '영등포구' : (11560),
        '용산구' : (11170),
        '은평구' : (11380),
        '종로구' : (11110),
        '중구' : (11140),
        '중랑구' : (11260)
}

reversedList = {v:k for k,v in sigunguCdList.items()}
df['guname'] = df['guname'].apply(lambda x : x.replace(x, reversedList[int(x)]))
df['1인당생활권공원면적'] = df['guname'].apply(lambda x : x.replace(x, str(parkareaperone[(x)]))).apply(lambda x : float(x))
df.drop('adzn_id', axis=1,inplace=True)
print(df)
df_mean = df.groupby('guname')['park_cnt'].agg(parkcntGumean = ('mean'))
df = pd.merge(df, df_mean, on='guname')

col_names = ['구이름','동이름','동별공원수','1인당생활권공원면적(m2)','구별평균공원수']
df.columns = col_names
df['rank_dense'] = df['1인당생활권공원면적(m2)'].rank(method='dense',ascending=False).apply(lambda x : int(x))
print(len(df['구이름'].unique()))
print(df.sample(n=100, replace=True))
output_file = 'city_park.json'
df = df.to_json(orient='records',force_ascii=False)

newdf = json.loads(df)

file_path = "./citypark.json"
data = {'data': newdf}  # Wrap `newdf` in a dictionary

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)