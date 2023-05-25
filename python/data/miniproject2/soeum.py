from fastapi import FastAPI, Request
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
import axios
import requests
import json, pandas as pd
import sys
import urllib.request
# from pprint import pprint
from geopy.geocoders import Nominatim
import folium

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

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

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
print('Connected to Mongodb...')


mydb = client['test']
mycoll = mydb['testdf']


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
        gangnam_noise_mean_real.append(gangnam_noise_mean[i][0])
        # gangnam_dong_list_real.append(ToKo(gangnam_dongs_list[i][0]))  # 한글변환
        gangnam_dong_list_real.append(gangnam_dongs_list[i][0])

    geumcheon_noise_mean = []
    geumcheon_noise_mean_real = []
    geumcheon_dong_list_real = []
    for i in range(len(geumcheon_dongs_list)):
        result = my_df2_geumcheon.groupby('administrative_district').get_group(f'{geumcheon_dongs_list[i][0]}')
        result.set_index('administrative_district', inplace=True)
        geumcheon_noise_mean.append(result.astype(float).mean().values)
        geumcheon_noise_mean_real.append(geumcheon_noise_mean[i][0])
        # geumcheon_dong_list_real.append(ToKo(geumcheon_dongs_list[i][0]))  # 한글변환
        geumcheon_dong_list_real.append(geumcheon_dongs_list[i][0])

    yeongdeungpo_noise_mean = []
    yeongdeungpo_noise_mean_real = []
    yeongdeungpo_dong_list_real = []
    for i in range(len(yeongdeungpo_dongs_list)):
        result = my_df2_yeongdeungpo.groupby('administrative_district').get_group(f'{yeongdeungpo_dongs_list[i][0]}')
        result.set_index('administrative_district', inplace=True)
        yeongdeungpo_noise_mean.append(result.astype(float).mean().values)
        yeongdeungpo_noise_mean_real.append(yeongdeungpo_noise_mean[i][0])
        yeongdeungpo_dong_list_real.append(ToKo(yeongdeungpo_dongs_list[i][0]))
        # yeongdeungpo_dong_list_real.append(yeongdeungpo_dongs_list[i][0])

    gangnam_df = pd.DataFrame({'administrative_district': gangnam_dong_list_real, 'noise': gangnam_noise_mean_real})
    # print(gangnam_df)
    # print('-' * 50)
    geumcheon_df = pd.DataFrame({'administrative_district': geumcheon_dong_list_real, 'noise': geumcheon_noise_mean_real})
    # print(geumcheon_df)
    # print('-' * 50)
    yeongdeungpo_df = pd.DataFrame({'administrative_district': yeongdeungpo_dong_list_real, 'noise': yeongdeungpo_noise_mean_real})
    # print(yeongdeungpo_df)
    # print('-' * 50)

    gangnam_gu_list = ['강남구'] * len(gangnam_df)
    geumcheon_gu_list = ['금천구'] * len(geumcheon_df)
    yeongdeungpo_gu_list = ['영등포구'] * len(yeongdeungpo_df)

    gangnam_soum_total = gangnam_df[['noise']].sum().values
    print('강남 전체 소음 평균 :', gangnam_soum_total[0] / len(gangnam_dongs))

    geumcheon_soum_total = geumcheon_df[['noise']].sum().values
    print('금천 전체 소음 평균 :', geumcheon_soum_total[0] / len(geumcheon_dongs))

    yeongdeungpo_soum_total = yeongdeungpo_df[['noise']].sum().values
    print('영등포 전체 소음 평균 :', yeongdeungpo_soum_total[0] / len(yeongdeungpo_dongs))
    print('-' * 50)


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
                mycol.insert_one(my_dict[key_num])
    except ValueError:
        print("just pass")
    return list(mycol.find({}))

@app.get('/')
async def healthCheck():
    return "GOOD"

@app.get('/getmongo')
async def getMongo():
    return list(mycol.find())

@app.get('/get_dong_data')  # 동 이름으로 검색
async def getdong(dong=None):
    info = []
    if dong is None:
        return "동 이름을 입력하세요."
    info.append(mycol.find_one({'administrative_district': dong}))
    result = info

    if result:
        return result
    else:
        return "검색 결과가 없습니다."

@app.get('/get_gu_data')  # 구 이름으로 검색
async def getgu(gu=None):
    info = []
    my_gu = ['강남', '영등포', '금천']
    if gu is None:
        return "구 이름을 입력하세요."
    for data in mycol.find():
        if data['autonomous_district'] == f'{gu}':
            info.append(data)
    result = info

    if result:
        return result
    else:
        return "검색 결과가 없습니다."

@app.get('/noise_in_map')  # 소음데이터 지도에 시각화
async def getplace(region=None):
    info = []
    my_gu = ['강남', '영등포', '금천']
    my_dong = []

    for i in range(len(list(mycol.find()))):
        for dong in mycol.find()[i]['administrative_district']:
            my_dong.append(dong)

    if region is None:
        return "지역 이름을 입력하세요."
    elif region in my_gu:
        for data in mycol.find():
            if data['autonomous_district'] == f'{region}구':
                info.append(data)

        geo_local = Nominatim(user_agent='South Korea')
        geo = geo_local.geocode(info[0]['autonomous_district'])
        x_y = [geo.latitude, geo.longitude]

        map_osm = folium.Map(location=[x_y[0], x_y[1]], zoom_start=14)
        for data in info:
            latitude = data['lat']
            longtitude = data['lng']
            dong_name = data['administrative_district']
            radius = data['noise']
            folium.Circle([latitude, longtitude], radius=radius * 10, color='red', fill_color='red', fill=False, popup=dong_name).add_to(map_osm)
        return map_osm.save('./mymap.html')
    elif len(region) == 2 and region[0] in my_dong and region[1] in my_dong:
        geo_local = Nominatim(user_agent='South Korea')
        geo = geo_local.geocode(region)
        x_y = [geo.latitude, geo.longitude]
        radius = mycol.find_one({'administrative_district': f'{region}동'})['noise']

        map_osm = folium.Map(location=[x_y[0], x_y[1]], zoom_start=14)
        folium.Circle([x_y[0], x_y[1]], radius=radius * 10, color='red', fill_color='red', fill=False, popup=f'{region}동').add_to(map_osm)

        return map_osm.save('./mymap.html')
    else:
        return "입력값을 다시 확인해주세요!" 