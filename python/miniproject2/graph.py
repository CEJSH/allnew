import json
import os.path
from pymongo import mongo_client
from fastapi import FastAPI
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
from datetime import datetime


app = FastAPI()

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

HOSTNAME = get_secret("ATLAS_Hostname")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")

client = mongo_client.MongoClient(f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}')
print('Connected to Mongodb....')

mydb = client['test']
mycol = mydb['construction']

@app.get('/getconstData')
def getconstData():
    return list(mycol.find({}))

def makechartTop10():
    constdata = getconstData()

    location_gu=[]
    location_dong=[]
    준공예정일=[]
    착공일=[]
    주용도=[]

    for i in constdata:
        location_gu.append(" ".join(i["대지위치"].split(" ")[0:2]))
        location_dong.append(i["대지위치"].split(" ")[2])
        준공예정일.append(i["준공예정일"])
        착공일.append(i["착공일"])
        주용도.append(i["주용도"])
    print("-"*50)
    print(len(location_dong))
    print("-"*50)
    const=pd.DataFrame({"구":location_gu,
                        "동":location_dong})


    const_less = const.groupby('동').count().sort_values(by="구", ascending=False).head(10)
    print(const_less)
    const_less.columns = ['동이름']
    xs=const_less.index.to_list()
            #dy_day(데이터 프레임)의 index(날짜, 시간)를 리스트로 저장 
    ys=const_less['동이름'].to_list()			#dy_day(테이터 프레임)의 volume 필드를 리스트로 저장
    plt.rc('font', family='AppleGothic')
    plt.figure(figsize=(10, 6))			#그래프 크기 지정
    plt.xlabel('동')				#그래프 x축 이름(label) 지정
    plt.ylabel('진행중인 공사 건수')				#그래프 y축 이름(label) 지정

    bar1 = plt.bar(xs, ys, width=0.6, color='blue', alpha=0.4)
    for i, j in enumerate(bar1) :
        plt.text(i, j.get_height() + 0.3, ys[i], ha= 'center')
    plt.show()
    plt.title(f'{datetime.today().strftime("%Y년%m월%d일")}자 동별 공사건수 상위Top10(5개구)')
    plt.savefig('chartmore.png')

    const_more = const.groupby('동').count().sort_values(by="구", ascending=True).head(10)
    print(const_less)

    const_more.columns = ['동']
    const_more.index.name = '동이름'
    const_more.plot(kind='bar',y=['동'])

    const_more.columns = ['동이름']
    xs=const_more.index.to_list()
            #dy_day(데이터 프레임)의 index(날짜, 시간)를 리스트로 저장 
    ys=const_more['동이름'].to_list()			#dy_day(테이터 프레임)의 volume 필드를 리스트로 저장
    plt.rc('font', family='AppleGothic')
    plt.figure(figsize=(10, 6))			#그래프 크기 지정
    plt.xlabel('동')				#그래프 x축 이름(label) 지정
    plt.ylabel('진행중인 공사 건수')				#그래프 y축 이름(label) 지정

    bar1 = plt.bar(xs, ys, width=0.6, color='blue', alpha=0.4)
    for i, j in enumerate(bar1) :
        plt.text(i, j.get_height() + 0.3, ys[i], ha= 'center')
    plt.show()
    plt.title(f'{datetime.today().strftime("%Y년%m월%d일")}자 동별 공사건수 하위Top10(5개구)')
    plt.savefig('chartless.png')
makechartTop10()