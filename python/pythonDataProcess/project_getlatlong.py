import json
import os.path
import folium, requests
import pandas as pd

filename = 'Seocho_seocho.csv'
newfilename = './' + filename.replace('.csv','.html')
df = pd.read_csv(filename, encoding='utf-8')

address = df['대지위치'].values
print(address)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        raise errorMsg


header = {'Authorization': 'KakaoAK ' + get_secret("kakao_apiKey")}
def getGeocoder(address):

    result = ""
    r = requests.get(url, headers=header)

    if r.status_code == 200:
        try:
            result_address = r.json()["documents"][0]["address"]
            result = result_address["y"], result_address["x"]
        except Exception as err:
            return None
    else:
        result = "ERROR[" + str(r.status_code) + "]"

    return result
foli_map = folium.Map(zoom_start=17)
num = 1
for i in address:
    
    address_word = i
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address_word
    
    address_latlng = getGeocoder(address_word)
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

foli_map.save(newfilename)
print('file saved...')
