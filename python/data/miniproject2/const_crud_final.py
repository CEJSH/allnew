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
from geopy.geocoders import Nominatim
import asyncio
from haversine import haversine

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

mydb = client['test']
mycoll = mydb['testdf']




@app.get('/')
async def healthCheck():
    return "OK"

@app.get('/getconstData')
async def getconstData():
    return list(mycol.find({}))

@app.get('/getdongconstuction')
async def getdongconstruction():
    construction = getconstData()
    gulist=[]
    donglist=[]
    for i in construction:
        print(i)
        gu = i['대지위치'].split(" ")[1]
        dong = i['대지위치'].split(" ")[2]
        gulist.append(gu)
        donglist.append(dong)
    print(gulist, donglist)
@app.get('/getParkdata')
async def getParkdata(sigudong=None):
    end_point = 'http://192.168.1.76:5000/data'
    parameters = '?'
    parameters += '구이름='
    parameters += sigudong
    url = end_point + parameters

    print('URL')
    print(url)
     
    result = json.loads(str(requests.get(url).text))
    averagearea = result[0]['1인당생활권공원면적(m2)']
    averagecount = round(result[0]['구별평균공원수'],2)
    rank = result[0]['rank_dense']
    if result == None:
        return None
    else:
        return averagearea, averagecount, rank


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
async def getsearchedareadata(sigudong):
    if sigudong is None:
        return "There's no data you want. input the region."
    threegudata = await getconstData()

    if sigudong[-1] == '구' and sigudong in sigunguCdList.keys():
        showList=[]
        address=[]
        print(1)
        print(sigunguCdList.keys())
        for i in threegudata:
            if sigudong in i['대지위치']:
                print(i['대지위치'])
                showList.append(i)
                address.append(i['대지위치'])
        await drawMap(address,sigudong)
        gu = address[0].split(" ")[1]
        park = await getParkdata(gu)
        print('park')
        return gu, len(address),park

    elif sigudong[-1] == '동' and sigudong in dongList:
        # myquery = {'대지위치' : {"$regex": f"^서울특별시 {sigudong}"}}
        showList=[]
        address=[]
        print(2)
        for i in threegudata:
            if sigudong in i['대지위치']:
                # print(i['대지위치'])
                showList.append(i)
                address.append(i['대지위치'])
        await drawMap(address,sigudong)
        gu = address[0].split(" ")[1]
        park = await getParkdata(gu)
        print('park')
        return gu, len(address),park
        
    elif (sigudong[-1] != '동' and sigudong[-1] != '구') and (sigudong + '동' in dongList or sigudong + '구' in sigunguCdList.keys()):
        showList=[]
        address=[]
        print(3)
        for i in threegudata:
            if sigudong in i['대지위치']:
                print(i['대지위치'])
                showList.append(i)
                address.append(i['대지위치'])
        print(len(address))
        if len(address) == 0:
            # foli_map = folium.Map(location=[37.498095, 127.027610], zoom_start=15)
            await saveMap(sigudong)
            return "There's no information about the region you want"
        else:
            print(address)
            await drawMap(address,sigudong)
            gu = address[0].split(" ")[1]
            park = await getParkdata(gu)
            print('park')
            return gu, len(address),park
    else:
        return "There's no information about the region you want"
       

@app.get('/getmorethantwomonthdata')
async def getmorethantwomonthdata(sigudong):
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
        await drawMap(address, sigudong)
        gu = address[0].split(" ")[1]
        park = await getParkdata(gu)
        return gu, len(address),park
    elif sigudong[-1] == '동' and sigudong in dongList:
        # myquery = {'대지위치' : {"$regex": f"^서울특별시 {sigudong}"}}
        showList=[]
        address=[]
        for i in threegudata:
            if sigudong in i['대지위치'] and datetime.datetime.strptime(i['준공예정일'],'%Y-%m-%d') > datetime.datetime.now() + relativedelta(months=2):
                showList.append(i)
                address.append(i['대지위치'])
        await drawMap(address,sigudong)
        gu = address[0].split(" ")[1]
        park = await getParkdata(gu)
        return gu, len(address),park
    elif (sigudong[-1] != '동' and sigudong[-1] != '구') and (sigudong + '동' in dongList or sigudong + '구' in sigunguCdList.keys()):
        showList=[]
        address=[]
        for i in threegudata:
            if sigudong in i['대지위치'] and datetime.datetime.strptime(i['준공예정일'],'%Y-%m-%d') > datetime.datetime.now() + relativedelta(months=2):
                showList.append(i)
                address.append(i['대지위치'])
        await drawMap(address,sigudong)
        gu = address[0].split(" ")[1]
        getParkdata(gu)
        park = await getParkdata(gu)
        return gu, len(address),park
    else:
        return "There's no information about the region you want"

@app.get('/admindelete')
async def admindelete():
    x = mycol.delete_many({})
    print(x.deleted_count, " documents deleted.")
    return list(mycol.find({}))

#################################################################################################################################################################################
header = {'Authorization': 'KakaoAK ' + get_secret("kakao_apiKey")}
global url
# foli_map = None
async def drawMap(address, sigudong):
    info = []
    my_gu = ['강남', '영등포', '금천']
    my_dong = []
    for i in range(len(list(mycoll.find()))):
        for dong in mycoll.find()[i]['administrative_district']:
            my_dong.extend(dong)
    foli_map = None
    layer = "Base"
    tileType = "png"
    tiles = f"http://api.vworld.kr/req/wmts/1.0.0/{'75AA8129-06F2-3A68-8C64-96E5728075DF'}/{layer}/{{z}}/{{y}}/{{x}}.{tileType}"
    attr = "Vworld"
    
    target = []
    geo_local = Nominatim(user_agent='South Korea')
    geo = geo_local.geocode(address[0])
    x_y = [geo.latitude, geo.longitude]

  
    foli_map = folium.Map(location=[x_y[0], x_y[1]], zoom_start=14)
    
    num = 1

    for i in address:
        
        address_word = i

        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address_word
        
        # geo_local = Nominatim(user_agent='South Korea')
        address_latlng = await getGeocoder(url)

        latitude = address_latlng[0]
        longitude = address_latlng[1]
        target.append((float(latitude),float(longitude)))

        # print('주소지 :', address_word)
        # print('위도 :', latitude)
        # print('경도 :', longitude)

        constrinfo = '공사장' + str(num)
        myicon = folium.Icon(color='red', icon='info-sign')
        popup = folium.Popup(folium.IFrame(f'{address_word}'), min_width=150, max_width=130)
        marker = folium.Marker([latitude, longitude], popup=popup).add_to(foli_map)

        folium.Circle([latitude, longitude], radius=60, color='#ffffgg', fill_color='#fffggg', fill=False, popup=constrinfo).add_to(foli_map)
        print("circle")
        num += 1 
    folium.TileLayer(tiles=tiles, attr=attr, overlay=True, control=True).add_to(foli_map)
    print(target)
    # return foli_map
    # foli_map.save('public/result.html')
    # print('file saved...')      

# async def saveMap(sigudong):   
    # global foli_map
    if sigudong is None:
        return "지역 이름을 입력하세요."
    elif sigudong[0:-1] in my_gu and sigudong[-1] == '구':
        for data in mycoll.find():
            if data['autonomous_district'] == sigudong:
                info.append(data)
        for data in info:
            latitude = data['lat']
            longtitude = data['lng']
            dong_name = data['administrative_district']
            radius = data['noise']
            popup = folium.Popup(folium.IFrame(f'{dong_name} : {radius}'), min_width=120, max_width=120)
            markercount = 0
            center = (float(latitude), float(longitude))

            for i in range(len(target)):
                if haversine(center,target[i]) < radius/100:
                    markercount += 1
                    print(int(haversine(center,target[i])))
            if markercount > 9:
                color = 'black'
            elif 9 >= markercount >= 6:
                color = 'red'
            elif 6 > markercount >= 4:
                color = 'orange'
            elif 4 > markercount >= 2:
                color = 'yellow'
            else:
                color = 'green'
            folium.Circle([latitude, longtitude], radius=radius * 10, color=color, fill_color=color, fill=False, popup=popup).add_to(foli_map)
            num +=1
            print('circle2')
        return foli_map.save('public/result.html'),

    elif len(sigudong) > 2 and sigudong[-1] == '동':
        user_dong = []
        info = list(mycoll.find())
        for data in info:
            if sigudong[:-1] in data['administrative_district']:
                user_dong.append(data)

        # geo_local = Nominatim(user_agent='South Korea')
        if sigudong == '삼성동':
            geo = geo_local.geocode('삼성1동')
        else:
            geo = geo_local.geocode(sigudong)
        
        # x_y = [geo.latitude, geo.longitude]
        # map_osm = folium.Map(location=[x_y[0], x_y[1]], zoom_start=14)
        folium.TileLayer(tiles=tiles, attr=attr, overlay=True, control=True).add_to(foli_map)

        for dong in user_dong:
            latitude = dong['lat']
            longtitude = dong['lng']
            dong_name = dong['administrative_district']
            radius = dong['noise']
            popup = folium.Popup(folium.IFrame(f'{dong_name} : {radius}'), min_width=120, max_width=120)
            markercount = 0
            center = (float(latitude), float(longitude))
            for i in range(len(target)):
                if await round(haversine(center,target[i]),2) < radius/100:
                    markercount += 1
            await print(markercount)
            if markercount > 9:
                color = 'black'
            elif 9 >= markercount >= 6:
                color = 'red'
            elif 6 > markercount >= 4:
                color = 'orange'
            elif 4 > markercount >= 2:
                color = 'yellow'
            else:
                color = 'green'
            folium.Circle([latitude, longtitude], radius=radius * 10, color=color, fill_color=color, fill=False, popup=popup).add_to(foli_map)
        return foli_map.save('public/result.html')


    elif sigudong in my_gu:
        for data in mycoll.find():
            if data['autonomous_district'] == f'{sigudong}구':
                info.append(data)
        folium.TileLayer(tiles=tiles, attr=attr, overlay=True, control=True).add_to(foli_map)
        for data in info:
            latitude = data['lat']
            longtitude = data['lng']
            dong_name = data['administrative_district']
            radius = data['noise']
            popup = folium.Popup(folium.IFrame(f'{dong_name} : {radius}'), min_width=120, max_width=120)
            markercount = 0
            center = (float(latitude), float(longitude))
            for i in range(len(target)):
                if haversine(center,target[i]) < radius/100:
                    print(haversine(center,target[i]))
                    markercount += 1
            
            if markercount > 9:
                color = 'black'
            elif 9 >= markercount >= 6:
                color = 'red'
            elif 6 > markercount >= 4:
                color = 'orange'
            elif 4 > markercount >= 2:
                color = 'yellow'
            else:
                color = 'green'
            folium.Circle([latitude, longtitude], radius=radius * 10, color=color, fill_color=color, fill=False, popup=popup).add_to(foli_map)

        return foli_map.save('public/result.html')
    # foli_map.save('public/result.html')
    # print('file saved...')
    elif len(sigudong) == 2 and sigudong[0] in my_dong and sigudong[1] in my_dong:  # '동'을 빼고 동 이름을 입력시
        user_dong = []
        info = list(mycoll.find())
        for data in info:
            if sigudong in data['administrative_district']:
                user_dong.append(data)

        folium.TileLayer(tiles=tiles, attr=attr, overlay=True, control=True).add_to(foli_map)

        for dong in user_dong:
            latitude = dong['lat']
            longtitude = dong['lng']
            dong_name = dong['administrative_district']
            radius = dong['noise']

            popup = folium.Popup(folium.IFrame(f'{dong_name} : {radius}'), min_width=120, max_width=120)
            markercount = 0
            center = (float(latitude), float(longitude))
            for i in range(len(target)):
                if haversine(center,target[i]) < radius/100:
                    print(haversine(center,target[i]))
                    markercount += 1
            
            if markercount > 9:
                color = 'black'
            elif 9 >= markercount >= 6:
                color = 'red'
            elif 6 > markercount >= 4:
                color = 'orange'
            elif 4 > markercount >= 2:
                color = 'yellow'
            else:
                color = 'green'
            folium.Circle([dong['lat'], dong['lng']], radius=radius * 10, color=color, fill_color=color, fill=False, popup=popup).add_to(foli_map)
        return foli_map.save('public/result.html')

    else:
        return "입력값을 다시 확인해주세요!" 

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



client_id = "HfVmgn5t2ERUmJngZKdN"  # 개발자센터에서 발급받은 Client ID 값
client_secret = "lBR7c4nAy7"  # 개발자센터에서 발급받은 Client Secret 값

def ToEn(koText):
    encText = urllib.parse.quote(koText)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        d = json.loads(result)
        # print('--- Korean to English --- ')
        # print('번역전 : ', koText)
        # print('번역후 : ', d['message']['result']['translatedText'])

    else:
        print("Error Code:" + rescode)

def ToKo(egText):
    kocText = urllib.parse.quote(egText)
    data = "source=en&target=ko&text=" + kocText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        d = json.loads(result)
        # print('--- English to Korean --- ')
        # print('번역전 : ', egText)
        # print('번역후 : ', d['message']['result']['translatedText'])
        return d['message']['result']['translatedText']

    else:
        print("Error Code:" + rescode)


@app.get('/jserver_to_mongo')
async def getjs():
    url = 'http://192.168.1.158:5000/DATA'
    result = json.loads(str(requests.get(url).text))

    full_df = pd.DataFrame(result)

    my_df = full_df[['autonomous_district', 'administrative_district', 'region', 'max_noise', 'min_noise', 'avg_noise', 'sensing_time']].replace('', 0).replace('Doksan-dong1', 'Doksan1-dong').replace('Dangsan-dong1', 'Dangsan1-dong').replace('Dangsan-dong2', 'Dangsan2-dong')

    myframe = my_df.loc[(my_df.autonomous_district == 'Gangnam-gu') | (my_df.autonomous_district == 'Gwanak-gu') | (my_df.autonomous_district == 'Geumcheon-gu') | (my_df.autonomous_district == 'Yeongdeungpo-gu')]

    # 강남구의 전체 동
    gangnam_dongs = my_df.loc[(my_df.autonomous_district == 'Gangnam-gu')][['administrative_district']].drop_duplicates()
    gangnam_dongs_list = gangnam_dongs.values

    # 금천구의 전체 동
    geumcheon_dongs = my_df.loc[(my_df.autonomous_district == 'Geumcheon-gu')][['administrative_district']].drop_duplicates()
    geumcheon_dongs_list = geumcheon_dongs.values

    # 영등포구의 전체 동
    yeongdeungpo_dongs = my_df.loc[(my_df.autonomous_district == 'Yeongdeungpo-gu')][['administrative_district']].drop_duplicates()
    yeongdeungpo_dongs_list = yeongdeungpo_dongs.values

    # 강남구 모든 동의 최대소음
    my_df2_gangnam = my_df.loc[(my_df.autonomous_district == 'Gangnam-gu')][['administrative_district', 'max_noise']].replace('', 0)

    # 금천구 모든 동의 최대소음
    my_df2_geumcheon = my_df.loc[(my_df.autonomous_district == 'Geumcheon-gu')][['administrative_district', 'max_noise']].replace('', 0)

    # 영등포구 모든 동의 최대소음
    my_df2_yeongdeungpo = my_df.loc[(my_df.autonomous_district == 'Yeongdeungpo-gu')][['administrative_district', 'max_noise']].replace('', 0)


    #######################################################소음 평균 구하기 및 좌표변환#######################################################

    gangnam_noise_mean = []
    gangnam_noise_mean_real = []
    gangnam_dong_list_real = []
    for i in range(len(gangnam_dongs_list)):
        result = my_df2_gangnam.groupby('administrative_district').get_group(f'{gangnam_dongs_list[i][0]}')
        result.set_index('administrative_district', inplace=True)
        gangnam_noise_mean.append(result.astype(float).mean().values)
        gangnam_noise_mean_real.append(round(gangnam_noise_mean[i][0]))
        gangnam_dong_list_real.append(ToKo(gangnam_dongs_list[i][0]))
        # gangnam_dong_list_real.append(gangnam_dongs_list[i][0])

    geumcheon_noise_mean = []
    geumcheon_noise_mean_real = []
    geumcheon_dong_list_real = []
    for i in range(len(geumcheon_dongs_list)):
        result = my_df2_geumcheon.groupby('administrative_district').get_group(f'{geumcheon_dongs_list[i][0]}')
        result.set_index('administrative_district', inplace=True)
        geumcheon_noise_mean.append(result.astype(float).mean().values)
        geumcheon_noise_mean_real.append(round(geumcheon_noise_mean[i][0]))
        geumcheon_dong_list_real.append(ToKo(geumcheon_dongs_list[i][0]))
        # geumcheon_dong_list_real.append(geumcheon_dongs_list[i][0])

    yeongdeungpo_noise_mean = []
    yeongdeungpo_noise_mean_real = []
    yeongdeungpo_dong_list_real = []
    for i in range(len(yeongdeungpo_dongs_list)):
        result = my_df2_yeongdeungpo.groupby('administrative_district').get_group(f'{yeongdeungpo_dongs_list[i][0]}')
        result.set_index('administrative_district', inplace=True)
        yeongdeungpo_noise_mean.append(result.astype(float).mean().values)
        yeongdeungpo_noise_mean_real.append(round(yeongdeungpo_noise_mean[i][0]))
        yeongdeungpo_dong_list_real.append(ToKo(yeongdeungpo_dongs_list[i][0]))
        # yeongdeungpo_dong_list_real.append(yeongdeungpo_dongs_list[i][0])

    gangnam_df = pd.DataFrame({'administrative_district': gangnam_dong_list_real, 'noise': gangnam_noise_mean_real})

    geumcheon_df = pd.DataFrame({'administrative_district': geumcheon_dong_list_real, 'noise': geumcheon_noise_mean_real})

    yeongdeungpo_df = pd.DataFrame({'administrative_district': yeongdeungpo_dong_list_real, 'noise': yeongdeungpo_noise_mean_real})

    gangnam_gu_list = ['강남구'] * len(gangnam_df)
    geumcheon_gu_list = ['금천구'] * len(geumcheon_df)
    yeongdeungpo_gu_list = ['영등포구'] * len(yeongdeungpo_df)

    gangnam_soum_total = gangnam_df[['noise']].sum().values
    gangnam_avg = round(gangnam_soum_total[0] / len(gangnam_dongs))

    geumcheon_soum_total = geumcheon_df[['noise']].sum().values
    geumcheon_avg = round(geumcheon_soum_total[0] / len(geumcheon_dongs))

    yeongdeungpo_soum_total = yeongdeungpo_df[['noise']].sum().values
    yeongdeungpo_avg = round(yeongdeungpo_soum_total[0] / len(yeongdeungpo_dongs))


    address_gangnam = gangnam_df['administrative_district']
    address_geumcheon = geumcheon_df['administrative_district']
    address_yeongdeungpo = yeongdeungpo_df['administrative_district']

    geo_local = Nominatim(user_agent='South Korea')
    def geocoding(address):
        try:
            geo = geo_local.geocode(address)
            x_y = [geo.latitude, geo.longitude]
            return x_y
        except:
            return [0,0]

    latitude_gangnam = []
    longitude_gangnam = []
    latitude_geumcheon = []
    longitude_geumcheon = []
    latitude_yeongdeungpo = []
    longitude_yeongdeungpo = []

    for i in address_gangnam:
        latitude_gangnam.append(geocoding(i)[0])
        longitude_gangnam.append(geocoding(i)[1])

    for j in address_geumcheon:
        latitude_geumcheon.append(geocoding(j)[0])
        longitude_geumcheon.append(geocoding(j)[1])

    for k in address_yeongdeungpo:
        latitude_yeongdeungpo.append(geocoding(k)[0])
        longitude_yeongdeungpo.append(geocoding(k)[1])

    addr_df_gangnam = pd.DataFrame({'autonomous_district': gangnam_gu_list, 'administrative_district': address_gangnam, 'noise': gangnam_noise_mean_real, 'lat': latitude_gangnam, 'lng': longitude_gangnam})
    addr_df_gangnam.set_index(['autonomous_district', 'administrative_district'])
    addr_df_geumcheon = pd.DataFrame({'autonomous_district': geumcheon_gu_list, 'administrative_district': address_geumcheon, 'noise': geumcheon_noise_mean_real, 'lat': latitude_geumcheon, 'lng': longitude_geumcheon})
    addr_df_geumcheon.set_index(['autonomous_district', 'administrative_district'])
    addr_df_yeongdeungpo = pd.DataFrame({'autonomous_district': yeongdeungpo_gu_list, 'administrative_district': address_yeongdeungpo, 'noise': yeongdeungpo_noise_mean_real, 'lat': latitude_yeongdeungpo, 'lng': longitude_yeongdeungpo})
    addr_df_yeongdeungpo.set_index(['autonomous_district', 'administrative_district'])
    
    gangnam_dict = addr_df_gangnam.to_dict(orient='index')
    geumcheon_dict = addr_df_geumcheon.to_dict(orient='index')
    yeongdeungpo_dict = addr_df_yeongdeungpo.to_dict(orient='index')

    my_dicts = [gangnam_dict, geumcheon_dict, yeongdeungpo_dict]
    try:
        for my_dict in my_dicts: 
            for key_num in range(len(my_dict)):
                if my_dict[key_num]['administrative_district'] == '도림동':
                    my_dict[key_num]['lat'] = 37.50872
                    my_dict[key_num]['lng'] = 126.90113
                mycoll.insert_one(my_dict[key_num])
    except ValueError:
        print("just pass")
    return list(mycoll.find({}))

