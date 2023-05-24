import urllib.request, datetime, math, json
import pandas as pd
import xml.etree.ElementTree as ET
import os.path

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
# secret_file = os.path.join(BASE_DIR, '../secret.json')

# with open(secret_file) as f:
#     secrets = json.loads(f.read())

# def get_secret(setting, secrets=secrets):
#     try:
#         return secrets[setting]
#     except KeyError:
#         errorMsg = "Set the {} environment variable.".format(setting)
#         return errorMsg
        
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

def getConstructionData(pageNo, numOfRows):
    end_point = 'http://apis.data.go.kr/1613000/ArchPmsService_v2/getApBasisOulnInfo'
    parameters = '?'
    parameters += "serviceKey=" + "JCJH%2BRLEhLAZ1j1f9kcUAu5OF4mDoTLQSP0B7ZddAoy7etL%2B0sSFda5ODHZRhcTVAOWlgEG9n4%2BU2FjiYELxpw%3D%3D"
    parameters += "&sigunguCd=" + str(11215)
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

bjdongCd = [10900]

for i in bjdongCd:
    bjdongCd = i
    dataList = []

    pageNo = 1 
    numOfRows = 10
    nPage = 0
    while(True):
        print('pageNo : %d, nPage : %d' % (pageNo, nPage))
        xmlData = getConstructionData(pageNo, numOfRows)
        print(xmlData)
        xmlTree = ET.fromstring(xmlData)

        if (xmlTree.find('header').find('resultMsg').text == 'NORMAL SERVICE.'):
            totalCount = int(xmlTree.find('body').find('totalCount').text)
            print('데이터 총 개수 : ', totalCount)  

            listTree = xmlTree.find('body').find('items').findall('item')
            print(listTree)

            for node in listTree:
                platPlc = node.find("platPlc").text
                mainPurpsCdNm = node.find("mainPurpsCdNm").text
                stcnsSchedDay = node.find("stcnsSchedDay").text
                stcnsDelayDay = node.find("stcnsDelayDay").text
                realStcnsDay = node.find("realStcnsDay").text
                jiyukCdNm = node.find("jiyukCdNm").text
                onedict = {'대지위치':platPlc, \
                        '주용도코드명':mainPurpsCdNm, '착공예정일':stcnsSchedDay, \
                        '착공연기일':stcnsDelayDay, '실제착공일':realStcnsDay, \
                        '지역코드명':jiyukCdNm}
                dataList.append(onedict)

            if totalCount == 0:
                break
            nPage = math.ceil(totalCount / numOfRows)
            if (pageNo == nPage):
                break 

            pageNo += 1
        else :
            break

    savedFilename = 'xx_construction_Gwangjin_'+str(bjdongCd)+'.csv'

    myframe = pd.DataFrame(dataList)
    myframe.to_csv(savedFilename)

    print(savedFilename + ' file saved..')
