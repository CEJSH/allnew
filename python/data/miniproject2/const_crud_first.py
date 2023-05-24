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

@app.get('/getmongo')
async def getMongo():
    return list(mycol.find().limit(50))

@app.get('/getthree_gudata')
def getprocessedData():
    dataList = []
    page = 1 
    perPage = 500
    nPage = 0
    
    while(True):
        print('page : %d, nPage : %d' % (page, nPage))
        getDataList = [getGangnamData(page,perPage),getYeongdeungpoData(page,perPage),getGeumcheonData(page,perPage)]
        for i in range(3):

            jsonData = getDataList[i]
            # print(jsonData)
            totalCount = jsonData['totalCount']
            

            for item in jsonData['data']:
                constCompleteD = item['준공예정일(사용승인예정일)']
                address = item['대지위치']
                constStartD = item['착공처리일']
                purpose = item['주용도']

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
# @app.get('/getYeongdeungpogdata')
# def getprocessedData():
#     dataList = []
#     page = 1 
#     perPage = 500
#     nPage = 0

#     while(True):
#         print('page : %d, nPage : %d' % (page, nPage))
#         jsonData = getYeongdeungpoData(page, perPage)
#         print(jsonData)
#         totalCount = jsonData['totalCount']

#         for item in jsonData['data']:
#             constCompleteD = item['준공예정일자']
#             address = item['대지위치']
#             constStartD = item['착공일자']
#             purpose = item['용도']

#             onedict = {'준공예정일':constCompleteD, \
#                         '대지위치':address, '착공일':constStartD, \
#                         '주용도':purpose}
#             dataList.append(onedict)
#         if totalCount == 0:
#             break
#         nPage = math.ceil(totalCount / perPage)
#         if (page == nPage):  
#             break  

#         pageNo += 1

#     myframe = pd.DataFrame(dataList)
#     print(myframe)
#     for i in range(len(myframe)):
#         try:
#             if myframe.iloc[i][0] is None:
#                 pass
#             elif datetime.datetime.strptime(myframe.iloc[i][0],'%Y-%m-%d') > datetime.datetime.now():
#                 print(myframe.iloc[i][0])
#                 mycol.insert_one(myframe.iloc[i].to_dict())
#         except ValueError:
#             print("Impossible", item)

# # @app.get('/getGeumcheondata')
# # def getprocessedData():
#     dataList = []
#     page = 1 
#     perPage = 500
#     nPage = 0
    
#     while(True):
#         print('page : %d, nPage : %d' % (page, nPage))
#         jsonData = getGeumcheonData(page, perPage)
#         print(jsonData)
#         totalCount = jsonData['totalCount']


#         for item in jsonData['data']:
#             constCompleteD = item['공사 종료일']
#             address = item['위치']
#             constStartD = item['착공일']
#             purpose = item['주용도']

#             onedict = {'준공예정일':constCompleteD, \
#                         '대지위치':address, '착공일':constStartD, \
#                         '주용도':purpose}
#             dataList.append(onedict)
#         if totalCount == 0:
#             break
#         nPage = math.ceil(totalCount / perPage)
#         if (page == nPage):  
#             break  

#         pageNo += 1

#     myframe = pd.DataFrame(dataList)
#     print(myframe)
#     for i in range(len(myframe)):
#         try:
#             if myframe.iloc[i][0] is None or datetime.datetime.strptime(myframe.iloc[i][0],'%Y-%m-%d') > datetime.datetime.strptime('2200-01-01','%Y-%m-%d'):
#                 pass
#             elif datetime.datetime.strptime(myframe.iloc[i][0],'%Y-%m-%d') > datetime.datetime.now():
#                 print(myframe.iloc[i][0])
#                 mycol.insert_one(myframe.iloc[i].to_dict())
#         except ValueError:
#             print("Impossible", item)



                    
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
# @app.get('/getlessthantwomonthadata')
# async def getlessthantwomonthadata(sigudong=None):
#     if sigudong is None:
#         return "There's no data you want. input the region."
#     threegudata = getconstData()
    
#     if sigudong[-1] == '구' and sigudong in sigunguCdList.keys():
#         showList=[]
#         print(sigunguCdList.keys())
#         for i in threegudata:
#             if sigudong in i['대지위치'] and datetime.datetime.strptime(i['준공예정일'],'%Y-%m-%d') < datetime.datetime.now() + relativedelta(months=2):
#                 showList.append(i)
#         print(showList)
#         return showList
#     elif sigudong[-1] == '동' and sigudong in dongList:
#         # myquery = {'대지위치' : {"$regex": f"^서울특별시 {sigudong}"}}
#         showList=[]
#         for i in threegudata:
#             if sigudong in i['대지위치'] and datetime.datetime.strptime(i['준공예정일'],'%Y-%m-%d') < datetime.datetime.now() + relativedelta(months=2):
#                 showList.append(i)
#         print(showList)
#         return showList

#     elif (sigudong[-1] != '동' and sigudong[-1] != '구') and (sigudong + '동' in dongList or sigudong + '구' in sigunguCdList.keys()):
#         showList=[]
#         for i in threegudata:
#             if sigudong in i['대지위치'] and datetime.datetime.strptime(i['준공예정일'],'%Y-%m-%d') < datetime.datetime.now() + relativedelta(months=2):
#                 showList.append(i)
#         print(showList)
#         return showList
#     else:
#         return "There's no information about the region you want"

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
async def userdelete():
    x = mycol.delete_many({})
    print(x.deleted_count, " documents deleted.")