from fastapi import FastAPI
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
from flask import Flask, request
import requests
import urllib.request
import json
import pandas as pd
import xml.etree.ElementTree as ET
import datetime
from dateutil.relativedelta import relativedelta
import math
import numpy as np
import time
import logging
import folium

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../../secret.json')

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
guList = ['강남구','금천구','영등포구']
dongList = ['역삼동','개포동','청담동','삼성동','대치동','신사동','논현동','압구정동','세곡동','자곡동','율현동','일원동','수서동','도곡동',
'가산동','독산동','시흥동','영등포동','영등포동1가','영등포동2가','영등포동3가','영등포동4가','영등포동5가','영등포동6가','영등포동7가','영등포동8가','여의도동','당산동1가','당산동2가','당산동3가','당산동4가','당산동5가','당산동6가','당산동',
'도림동','문래동1가','문래동2가','문래동3가','문래동4가','문래동5가','문래동6가','양평동1가','양평동2가','양평동3가','양평동4가','양평동5가','양평동6가','양화동','신길동','대림동','양평동']
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
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

logging.basicConfig(level=logging.INFO)  # Configure logging

def getGangnamData(page, perPage):

    end_point = 'https://api.odcloud.kr/api/15108269/v1/uddi:91a5844a-a287-4802-b16c-cc7bafbe9582'
    parameters = '?'
    parameters += "serviceKey=" + get_secret("data_apiKey")
    parameters += "&page=" + str(page) 
    parameters += "&perPage=" + str(perPage) 
    parameters += "&returnType=" + "JSON" 
    url = end_point + parameters

    print('URL')
    print(url)

    result = getRequestUrl(url)
    if (result == None):
        return None
    else:
        return json.loads(result)

def getYeongdeungpoData(page, perPage):

    end_point = 'https://api.odcloud.kr/api/15108024/v1/uddi:52faa3b2-91d0-4797-88bf-fee0b99d9532'
    parameters = '?'
    parameters += "serviceKey=" + get_secret("data_apiKey")
    parameters += "&page=" + str(page) 
    parameters += "&perPage=" + str(perPage) 
    parameters += "&returnType=" + "JSON" 
    url = end_point + parameters

    print('URL')
    print(url)

    result = getRequestUrl(url)
    if (result == None):
        return None
    else:
        return json.loads(result)

def getGeumcheonData(page, perPage):

    end_point = 'https://api.odcloud.kr/api/15108273/v1/uddi:3ddac34e-433c-4754-b151-f943e9bfee87'
    parameters = '?'
    parameters += "serviceKey=" + get_secret("data_apiKey")
    parameters += "&page=" + str(page) 
    parameters += "&perPage=" + str(perPage) 
    parameters += "&returnType=" + "JSON" 
    url = end_point + parameters

    print('URL')
    print(url)

    result = getRequestUrl(url)
    if (result == None):
        return None
    else:
        return json.loads(result)

HOSTNAME = get_secret("ATLAS_Hostname")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")

client = mongo_client.MongoClient(f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}')
print('Connected to Mongodb....')

mydb = client['test']
mycol = mydb['testdb']

@app.get('/')
async def healthCheck():
    return "OK"

@app.get('/getconstData')
async def getconstData():
    return list(mycol.find({}))

@app.get('/getParkdata')
async def getParkdata(sigungu=None):

    end_point = 'http://192.168.1.76:5000/data'
    parameters = '?'
    parameters += '동이름='
    parameters += sigungu
    url = end_point + parameters

    print('URL')
    print(url)

    result = json.loads(str(requests.get(url).text))
    if result == None:
        return None
    else:
        return result

@app.get('/getthree_gudata')
async def getprocessedData():
    dataList = []
    page = 1 
    perPage = 500
    nPage = 0
    
    while(True):
        print('page : %d, nPage : %d' % (page, nPage))
        getDataList = [getGangnamData(page,perPage),getYeongdeungpoData(page,perPage),getGeumcheonData(page,perPage)]
        for i in range(3):
            jsonData = getDataList[i]
            totalCount = jsonData['totalCount']
            if i == 0:
                    for item in jsonData['data']:
                        constCompleteD = item['준공예정일(사용승인예정일)']
                        address = item['대지위치']
                        constStartD = item['착공처리일']
                        purpose = item['주용도']
                        if address.find(' 외') > 0:
                            start = address.find(' 외')
                            address = address[:start]
                            onedict = {'준공예정일':constCompleteD, \
                                        '대지위치':address, '착공일':constStartD, \
                                        '주용도':purpose}
                            dataList.append(onedict)
            elif i == 1:
                    for item in jsonData['data']:
                        constCompleteD = item['준공예정일자']
                        address = item['대지위치']
                        constStartD = item['착공일자']
                        purpose = item['용도']
                        if address.find(' 외') > 0:
                            start = address.find(' 외')
                            address = address[:start]
                            onedict = {'준공예정일':constCompleteD, \
                                        '대지위치':address, '착공일':constStartD, \
                                        '주용도':purpose}
                            dataList.append(onedict)
            elif i == 2:
                    for item in jsonData['data']:
                        constCompleteD = item['공사 종료일']
                        address = item['위치']
                        constStartD = item['착공일']
                        purpose = item['주용도']
                        if address.find(' 외') > 0:
                            start = address.find(' 외')
                            address = address[:start]
                            onedict = {'준공예정일':constCompleteD, \
                                        '대지위치':address, '착공일':constStartD, \
                                        '주용도':purpose}
                            dataList.append(onedict)
        if totalCount == 0:
            break
        nPage = math.ceil(totalCount / perPage)
        if (page == nPage):  
            break  

        pageNo += 1

    myframe = pd.DataFrame(dataList)
    print(myframe)
    for i in range(len(myframe)):
        try:
            if myframe.iloc[i][0] is None:
                pass
            elif datetime.datetime.strptime(myframe.iloc[i][0],'%Y-%m-%d') > datetime.datetime.now():
                print(myframe.iloc[i][0])
                mycol.insert_one(myframe.iloc[i].to_dict())
        except ValueError:
            print("Impossible", item)
    return list(mycol.find({}))

@app.get('/getsearchedareadata')
async def getsearchedareadata(sigudong=None):
    if sigudong is None:
        return "There's no data you want. input the region."
    threegudata = await getconstData()
    
    if sigudong[-1] == '구' and sigudong in sigunguCdList.keys():
        showList=[]
        address=[]
        print(sigunguCdList.keys())
        for i in threegudata:
            if sigudong in i['대지위치']:
                showList.append(i)
                address.append(i['대지위치'])
        await drawMap(address)
        print(showList)
        return showList
    elif sigudong[-1] == '동' and sigudong in dongList:
        # myquery = {'대지위치' : {"$regex": f"^서울특별시 {sigudong}"}}
        showList=[]
        address=[]
        for i in threegudata:
            if sigudong in i['대지위치']:
                showList.append(i)
                address.append(i['대지위치'])
        await drawMap(address)
        print(showList)
        return showList

    elif (sigudong[-1] != '동' and sigudong[-1] != '구') and (sigudong + '동' in dongList or sigudong + '구' in sigunguCdList.keys()):
        showList=[]
        address=[]
        for i in threegudata:
            if sigudong in i['대지위치']:
                showList.append(i)
                address.append(i['대지위치'])
        await drawMap(address)
        print(showList)
        return showList
    else:
        return "There's no information about the region you want"
       


@app.get('/getmorethantwomonthadata')
async def getmorethantwomonthdata(sigudong=None):
    if sigudong is None:
        return "There's no data you want. input the region."
    threegudata = await getconstData()
    
    if sigudong[-1] == '구' and sigudong in sigunguCdList.keys():
        showList=[]
        address=[]
        print(sigunguCdList.keys())
        for i in threegudata:
            if sigudong in i['대지위치'] and datetime.datetime.strptime(i['준공예정일'],'%Y-%m-%d') > datetime.datetime.now() + relativedelta(months=2):
                showList.append(i)
                address.append(i['대지위치'])
        await drawMap(address)

        return showList
    elif sigudong[-1] == '동' and sigudong in dongList:
        # myquery = {'대지위치' : {"$regex": f"^서울특별시 {sigudong}"}}
        showList=[]
        for i in threegudata:
            if sigudong in i['대지위치'] and datetime.datetime.strptime(i['준공예정일'],'%Y-%m-%d') > datetime.datetime.now() + relativedelta(months=2):
                showList.append(i)
                address.append(i['대지위치'])
        await drawMap(address)
        return showList

    elif (sigudong[-1] != '동' and sigudong[-1] != '구') and (sigudong + '동' in dongList or sigudong + '구' in sigunguCdList.keys()):
        showList=[]
        for i in threegudata:
            if sigudong in i['대지위치'] and datetime.datetime.strptime(i['준공예정일'],'%Y-%m-%d') > datetime.datetime.now() + relativedelta(months=2):
                showList.append(i)
        await drawMap(address)
        return showList
    else:
        return "There's no information about the region you want"

@app.get('/admindelete')
async def admindelete():
    x = mycol.delete_many({})
    print(x.deleted_count, " documents deleted.")
    return list(mycol.find({}))

filename = './result.html'

header = {'Authorization': 'KakaoAK ' + get_secret("kakao_apiKey")}
global url
async def drawMap(address):
    foli_map = folium.Map(zoom_start=17)
    num = 1
    print(address)
    for i in address:
        
        address_word = i

        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address_word
        
        address_latlng = await getGeocoder(url)
        latitude = address_latlng[0]
        longitude = address_latlng[1]

        print('주소지 :', address_word)
        print('위도 :', latitude)
        print('경도 :', longitude)

        constrinfo = '공사장' + str(num)
        myicon = folium.Icon(color='red', icon='info-sign')
        marker = folium.Marker([latitude, longitude], popup=constrinfo).add_to(foli_map)

        folium.Circle([latitude, longitude], radius=60, color='blue', fill_color='#D5F5E3', fill=False, popup=constrinfo).add_to(foli_map)
        num += 1 

    foli_map.save(filename)
    print('file saved...')

async def getGeocoder(url):
    print(url)
    result = ""
    r = requests.get(url, headers=header)

    if r.status_code == 200:
        try:
            print(r.text)
            result_address = r.json()["documents"][0]["address"]
            result = result_address["y"], result_address["x"]
        except Exception as err:
            print('----------------------------------------------------------------------------------------')
            print(err)
            return None
    else:
        result = "ERROR[" + str(r.status_code) + "]"

    return result