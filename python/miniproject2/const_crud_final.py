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
from folium import utilities
from pyppeteer import launch
import matplotlib.pyplot as plt


# pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
# plt.rc('font', family="AppleGothic")
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
guList = ['강남구','금천구','영등포구','관악구']
dongList = ['후암동','용산2가동','남영동','청파동','원효로1동','원효로2동','효창동','용문동','한강로동','이촌1동','이촌2동','이태원1동','이태원2동','한남동','서빙고동','보광동','봉천동','신림동','남현동','역삼동','개포동','청담동','삼성동','대치동','신사동','논현동','압구정동','세곡동','자곡동','율현동','일원동','수서동','도곡동',
'가산동','독산동','시흥동','영등포동','영등포동1가','영등포동2가','영등포동3가','영등포동4가','영등포동5가','영등포동6가','영등포동7가','영등포동8가','여의도동','당산동1가','당산동2가','당산동3가','당산동4가','당산동5가','당산동6가','당산동',
'도림동','문래동1가','문래동2가','문래동3가','문래동4가','문래동5가','문래동6가','양평동1가','양평동2가','양평동3가','양평동4가','양평동5가','양평동6가','양화동','신길동','대림동','양평동']
target = 'map'
async def map_to_png(foli_map):
    html = foli_map.get_root().render()
    browser=await launch(options={'args': ['--no-sandbox']})

    page = await browser.newPage()
    with utilities.temp_html_filepath(html) as fname:
        await page.goto('file://{path}'.format(path=fname))

    img_data = await page.screenshot({'path': f'./out_img.png', 'fullPage': 'true', })
    await browser.close()

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

def getGwanakData(page, perPage):

    end_point = 'https://api.odcloud.kr/api/15117092/v1/uddi:3aff0031-e07a-4673-aac6-d7cbbfd3c642'
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

def getYongsanData(page, perPage):

    end_point = 'https://api.odcloud.kr/api/15108231/v1/uddi:76360492-c5bd-4ffb-a4ab-b66d4787216e'
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
mycol = mydb['construction']

mydb = client['test']
mycoll = mydb['testdb']



# @app.get('/')
# async def healthCheck():
    # return "OK"

# get all the construction data in the form of list from mongodb 
@app.get('/getconstData')
async def getconstData():
    return list(mycol.find({}))

# get information about city park in json server and show them in result html with the map.
#even you just put only dong, the algorithm match the right district and find the data.
#it is possible by the reason of using response
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


@app.get('/getfive_gudata')
async def getprocessedData():
    dataList = []
    page = 1 
    perPage = 500
    nPage = 0
    
    while(True):
        print('page : %d, nPage : %d' % (page, nPage))
        getDataList = [getGangnamData(page,perPage),getYeongdeungpoData(page,perPage),getGeumcheonData(page,perPage),getGwanakData(page, perPage),getYongsanData(page, perPage)]
        for i in range(5):
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
            elif i == 3:
                    for item in jsonData['data']:
                        address = item['대지위치']
                        constStartD = datetime.datetime.strptime(item['착공처리일'],'%Y-%m-%d')
                        constCompleteD = (datetime.datetime.strptime(item['착공처리일'],'%Y-%m-%d') + relativedelta(years=1)).strftime('%Y-%m-%d')
                        purpose = item['주용도']
                        if address.find(' 외') > 0:
                            start = address.find(' 외')
                            address = address[:start]
                        onedict = {'준공예정일':constCompleteD, \
                                    '대지위치':address, '착공일':constStartD, \
                                    '주용도':purpose}
                        dataList.append(onedict)
            elif i == 4:
                    for item in jsonData['data']:
                        address = item['대지위치']
                        if item['착공처리일'] is None:
                            pass
                        else:
                            constStartD = datetime.datetime.strptime(item['착공처리일'],'%Y-%m-%d')
                            constCompleteD = (datetime.datetime.strptime(item['착공처리일'],'%Y-%m-%d') + relativedelta(years=1)).strftime('%Y-%m-%d')
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
            elif type(myframe.iloc[i][0]) == datetime.datetime and myframe.iloc[i][0] > datetime.datetime.now():
                print(myframe.iloc[i][0])
                mycol.insert_one(myframe.iloc[i].to_dict())
            elif type(myframe.iloc[i][0]) == str and datetime.datetime.strptime(myframe.iloc[i][0],'%Y-%m-%d') > datetime.datetime.now():
                print(myframe.iloc[i][0])
                mycol.insert_one(myframe.iloc[i].to_dict())
        except ValueError:
            print("Impossible", item)                                                                         
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


    const_more = const.groupby('동').count().sort_values(by="구", ascending=True).head(20)
    print(const_more)
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
    plt.title(f'{datetime.today().strftime("%Y년%m월%d일")}자 동별 공사건수 상위Top10(5개구)')
    plt.savefig('chartmore.png')

    const_less = const.groupby('동').count().sort_values(by="구", ascending=False).head(10)
    print(const_less)

    const_less.columns = ['동']
    const_less.index.name = '동이름'
    const_less.plot(kind='bar',y=['동'])

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
    plt.title(f'{datetime.today().strftime("%Y년%m월%d일")}자 동별 공사건수 하위Top10(5개구)')
    plt.savefig('chartless.png')

@app.get('/getSearchedAreadata')
async def getSearchedAreadata(sigudong):
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
        park = await getParkdata(gu)
        return gu, len(address),park
    else:
        return foli_map.save('public/result.html')


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
    my_gu = ['강남', '영등포', '금천', '관악','용산']
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
            center = (float(latitude), float(longtitude))

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
        await map_to_png(foli_map)
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
                if (round(haversine(center,target[i]),2)) < radius/100:
                    markercount += 1
            print(markercount)
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
        await map_to_png(foli_map)
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
            center = (float(latitude), float(longtitude))
            for i in range(len(target)):
                if haversine(center,target[i]) < radius/100:
                    print('here')
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
        await map_to_png(foli_map)
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
            center = (float(latitude), float(longtitude))
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
        await map_to_png(foli_map)
        return foli_map.save('public/result.html')

    else:
        return foli_map.save('public/result.html')

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

@app.get('/get_topfive_noise')
async def getTopFiveNoise():
    full_data_list = list(mycoll.find())
    gangnam_dongs = []
    gangnam_noises = []

    geumcheon_dongs = []
    geumcheon_noises = []

    yeongdeungpo_dongs = []
    yeongdeungpo_noises = []

    gwanak_dongs = []
    gwanak_noises = []

    yongsan_dongs = []
    yongsan_noises = []

    for data in full_data_list:
        if data['autonomous_district'] == '강남구':
            gangnam_dongs.append(data['administrative_district'])
            gangnam_noises.append(data['noise'])
        elif data['autonomous_district'] == '금천구':
            geumcheon_dongs.append(data['administrative_district'])
            geumcheon_noises.append(data['noise'])
        elif data['autonomous_district'] == '영등포구':
            yeongdeungpo_dongs.append(data['administrative_district'])
            yeongdeungpo_noises.append(data['noise'])
        elif data['autonomous_district'] == '관악구':
            gwanak_dongs.append(data['administrative_district'])
            gwanak_noises.append(data['noise'])
        elif data['autonomous_district'] == '용산구':
            yongsan_dongs.append(data['administrative_district'])
            yongsan_noises.append(data['noise'])

    gangnam_df = pd.DataFrame({'동 이름': gangnam_dongs, '소음도': gangnam_noises})
    gangnam_df_st = gangnam_df.sort_values('소음도', ascending=False).set_index(['동 이름']).head(5)

    geumcheon_df = pd.DataFrame({'동 이름': geumcheon_dongs, '소음도': geumcheon_noises})
    geumcheon_df_st = geumcheon_df.sort_values('소음도', ascending=False).set_index(['동 이름']).head(5)

    yeongdeungpo_df = pd.DataFrame({'동 이름': yeongdeungpo_dongs, '소음도': yeongdeungpo_noises})
    yeongdeungpo_df_st = yeongdeungpo_df.sort_values('소음도', ascending=False).set_index(['동 이름']).head(5)

    gwanak_df = pd.DataFrame({'동 이름': gwanak_dongs, '소음도': gwanak_noises})
    gwanak_df_st = gwanak_df.sort_values('소음도', ascending=False).set_index(['동 이름']).head(5)

    yongsan_df = pd.DataFrame({'동 이름': yongsan_dongs, '소음도': yongsan_noises})
    yongsan_df_st = yongsan_df.sort_values('소음도', ascending=False).set_index(['동 이름']).head(5)


    gangnam_df_st.plot(kind='bar', title='강남구 소음도 TOP5', figsize=(10, 6), legend=True)
    plt.xticks(rotation=0)
    filename = './public/강남구.png'
    plt.savefig(filename, dpi=400, bbox_inches='tight')

    geumcheon_df_st.plot(kind='bar', title='금천구 소음도 TOP5', figsize=(10, 6), legend=True)
    plt.xticks(rotation=0)
    filename = './public/금천구.png'
    plt.savefig(filename, dpi=400, bbox_inches='tight')

    yeongdeungpo_df_st.plot(kind='bar', title='영등포구 소음도 TOP5', figsize=(10, 6), legend=True)
    plt.xticks(rotation=0)
    filename = './public/영등포구.png'
    plt.savefig(filename, dpi=400, bbox_inches='tight')

    gwanak_df_st.plot(kind='bar', title='관악구 소음도 TOP5', figsize=(10, 6), legend=True)
    plt.xticks(rotation=0)
    filename = './public/관악구.png'
    plt.savefig(filename, dpi=400, bbox_inches='tight')

    yongsan_df_st.plot(kind='bar', title='용산구 소음도 TOP5', figsize=(10, 6), legend=True)
    plt.xticks(rotation=0)
    filename = './public/용산구.png'
    plt.savefig(filename, dpi=400, bbox_inches='tight')

    print(gangnam_df_st)
    print(geumcheon_df_st)
    print(yeongdeungpo_df_st)
    print(gwanak_df_st)
    print(yongsan_df_st)

    return 'good'



