from fastapi import FastAPI
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
import requests
import urllib.request
import json
import pandas as pd
import xml.etree.ElementTree as ET
import datetime
import math
import numpy as np
import time

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../../secret.json')

sigunguCdList = {
        '강남구' : (11680,[10100,10300,10400,10500,10600,10700,10800,11000,11100,11200,11300,11500,11800]),
        '관악구' : (11620,[10100,10200,10300]),
        '강북구' : (11305,[10100,10200,10300,10400]),
        '강동구' : (11740,[10100,10200,10300,10500,10600,10700,10800,10900,11000]),
        '강서구' : (11500,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000,11100,11200,11300]),
        '광진구' : (11215,[10100,10200,10300,10500,10700,10900]),
        '구로구' : (11530,[10200,10300,10600,10700,10800,10900,11000,11100,11200]),
        '금천구' : (11545,[10100,10200,10300]),
        '노원구' : (11350,[10200,10300,10400,10500,10600]),
        '도봉구' : (11320,[10500,10600,10700,10800]),
        '동대문구' : (11230,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000]),
        '동작구' : (11590,[10100,10200,10300,10400,10500,10600,10700,10800,10900]),
        '마포구' : (11440,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000,11100,11200,11300,11400,11500,11600,11700,11800,12000,12100,12200,12300,12400,12500,12600,12700]),
        '서대문구' : (11410,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000,11100,11200,11300,11400,11500,11600,11700,11800,11900,12000]),
        '서초구' : (11650,[10100,10200,10300,10400,10600,10700,10800,10900,11000,11100]),
        '성동구' : (11200,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000,11100,11200,11300,11400,11500,11800,12200]),
        '성북구' : (11290,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000,11100,11200,11300,11400,11500,11600,11700,11800,11900,12000,12100,12200,12300,12400,12500,12600,12700,12800,12900,13000,
13100,13200,13300,13400,13500,13600,13700,13800,13900]),
        '송파구' : (11710,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11100,11200,11300,11400]),

        '양천구' : (11470,[10100,10200,10300]),
        '영등포구' : (11560,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000,11100,11200,11300,11400,11500,11600,11700,11800,11900,12000,12100,12200,12300,12400,12500,12600,12700,
12800,12900,13000,13100,13200,13300,13400]),
        '용산구' : (11170,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000,11100,11200,11300,11400,11500,11600,11700,11800,11900,12000,12100,12200,12300,12400,12500,12600,12700,
12800,12900,13000,13100,13200,13300,13400,13500,13600]),
        '은평구' : (11380,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000,11400]),
        '종로구' : (11110,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000,11100,11200,11300,11400,11500,11600,11700,11800,11900,12000,12100,12200,12300,12400,12500,12600,12700,
12800,12900,13000,13100,13200,13300,13400,13500,13600,13700,13800,13900,14000,14100,14200,14300,14400,14500,14600,14700,14800,14900,15000,15100,15200,15300,15400,15500,15600,15700,15800,15900,16000,16100,16200,16300,16400,16500,16600,16700,16800,16900,17000,17100,17200,17300,17400,17500,17600,17800,17900,18000,
18100,18200,18300,18400,18500,18600,18700]),
        '중구' : (11140,[10100,10200,10300,10400,10500,10600,10700,10800,10900,11000,11100,11200,11300,11400,11500,11600,11700,11800,11900,12000,12100,12200,12300,12400,12500,12600,12700,
12800,12900,13000,13100,13200,13300,13400,13500,13600,13700,13800,13900,14000,14100,14200,14300,14400,14500,14600,14700,14800,14900,15000,15100,15200,15300,15400,15500,15600,15700,15800,15900,16000,16100,16200,16300,16400,16500,16600,16700,16800,16900,17000,17100,17200,17300,17400]),

        '중랑구' : (11260,[10100,10200,10300,10400,10500,10600])
}

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

def getConstructionData(sigunguCd, bjdongCd, pageNo, numOfRows):

    end_point = 'https://api.odcloud.kr/api/15108269/v1/uddi:91a5844a-a287-4802-b16c-cc7bafbe9582'
    parameters = '?'
    parameters += "serviceKey=" + "pz8AHfdVgweD18FrLox%2Bf84re1suiNrLxNSkqRY8qEqQgWkiIae1tYmHahgYbnW9mPZkDLQhzA70tsy4mCqXPg%3D%3D"
    parameters += "&sigunguCd=" + str(sigunguCd)
    parameters += "&bjdongCd=" +str(bjdongCd)
    parameters += "&pageNo=" + str(pageNo) 
    parameters += "&numOfRows=" + str(numOfRows) 
    url = end_point + parameters

    print('URL')
    print(url)

    result = getRequestUrl(url)
    if (result == None):
        return None
    else:
        return result

        
dataList = []

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

@app.get('/getmongo')
async def getMongo():
    return list(mycol.find().limit(50))

@app.get('/getdata')
def getprocessedData(sigungu):
    if sigungu is None:
        sigungu = [10100]
        print(sigungu)
    elif sigungu in sigunguCdList:
        sigunguCd = sigunguCdList[sigungu][0]
        print(sigunguCd)
        bjdongCd = sigunguCdList[sigungu][1]
        print(bjdongCd)
    

        for i in bjdongCd:
            bjdongCd = i
            pageNo = 1 
            numOfRows = 100
            nPage = 0
            
            while(True):
                print('pageNo : %d, nPage : %d' % (pageNo, nPage))
                xmlData = getConstructionData(sigunguCd, bjdongCd, pageNo, numOfRows)
                print(xmlData)
                xmlTree = ET.fromstring(xmlData)

                if (xmlTree.find('header').find('resultMsg').text == 'NORMAL SERVICE.'):
                    totalCount = int(xmlTree.find('body').find('totalCount').text)
                    print('데이터 총 개수 : ', totalCount)

                    listTree = xmlTree.find('body').find('items').findall('item')
                    print(listTree)
                    
                    for node in listTree:
                        if node.find('stcnsSchedDay').text != ' ' or node.find('realStcnsDay').text != ' ':
                            if node.find('stcnsSchedDay').text != ' ':
                                if " " in str(node.find('stcnsSchedDay').text):
                                    node.find('stcnsSchedDay').text = np.nan
                            elif node.find('realStcnsDay').text != ' ':
                                if " " in str(node.find('realStcnsDay').text):
                                    node.find('realStcnsDay').text = np.nan

                        stcnsSchedDay_text = node.find("stcnsSchedDay").text
                        realStcnsDay_text = node.find("realStcnsDay").text
                                
                        try:
                            if stcnsSchedDay_text or realStcnsDay_text:  # Check if both attributes are not empty
                                stcnsSchedDay = float(stcnsSchedDay_text)
                                realStcnsDay = float(realStcnsDay_text)
                                if stcnsSchedDay > 20221201 or realStcnsDay > 20221201:
                                    platPlc = node.find("platPlc").text
                                    sigunguCd = node.find("sigunguCd").text
                                    mainPurpsCdNm = node.find("mainPurpsCdNm").text
                                    stcnsSchedDay = float(node.find("stcnsSchedDay").text)
                                    realStcnsDay = float(node.find("realStcnsDay").text)
                                    jiyukCdNm = node.find("jiyukCdNm").text
                                    onedict = {'대지위치':platPlc, \
                                            '주용도코드명':mainPurpsCdNm, '시군구코드':sigunguCd, '착공예정일':stcnsSchedDay, \
                                            '실제착공일':realStcnsDay, \
                                            '지역코드명':jiyukCdNm}
                                    dataList.append(onedict)
                                    mycol.insert_one(onedict)
                            
                            else :
                                    break
                        except ValueError:
                            # Handle the case where the conversion to float fails
                            print("Failed to convert to float:", stcnsSchedDay_text, realStcnsDay_text)
                            
                        
                    if totalCount == 0:
                        break
                    nPage = math.ceil(totalCount / numOfRows)
                    if (pageNo == nPage):
                        
                        break 

                    pageNo += 1
                else :
                    break
        # mycol.insert_many(dataList)            
    # savedFilename = 'newGwanak.csv'
    # myframe = pd.DataFrame(dataList)
    # return myframe
# @app.get('/useradd')
# async def spotadd(address, usagecode,constPred,constReal,regioncode):
    # for data in dataList:
        # if dataList is None:
            # return "there's no data"
        # else:
            # spot = dict(address=myframe['대지위치'][i], usagecode=myframe['주용도코드명'][i], constPred=myframe['착공예정일'][i], constReal=myframe['실제착공일'][i],
            # regioncode=myframe['지역코드명'][i])
            # mycol.insert_many(dataList)
            # result = mycol.find_one({'id':id})
    # return list(mycol.find().limit(10))

# @app.get('/userupdate')
# async def userupdate(id=None, name=None):
#     if (id and name) is None:
#         return "id, name을 입력하세요."
#     else:
#         user = mycol.find_one({"id": id})
#         if user:
#             filter = {'id':id}
#             data = {"$set":{'name':name}}
#             mycol.update_one(filter,data)
#             result = mycol.find_one({'id':id})
#             return result
#         else:
#             return f"id = {id} 데이터가 존재하지 않습니다."

@app.get('/userdelete')
async def userdelete(sigunguCd=None, bjdongCd=None):
    myquery = {'대지위치' : {"$regex": f"^서울특별시 {sigunguCd}"}}
    if sigunguCd is None:
        return "시군구명을 입력하세요."
    else:
        user = mycol.find_one(myquery)
        if user:
            mycol.delete_many(myquery)
            return list(mycol.find().limit(50))
        else:
            return f"bjdongCd = {bjdongCd} 데이터가 존재하지 않습니다."