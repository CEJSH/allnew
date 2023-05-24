import urllib.request, datetime, math, json
import pandas as pd
import xml.etree.ElementTree as ET
import os.path
import numpy as np

        
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
    parameters += "serviceKey=" + "U6mE%2FsVh5ntHHu%2B1itc5F4n7G47gHusiLVHD1%2B5ofQfZBK8Vh%2BFw4ByUTXcW9Avf4O0MO%2BNTI3RTBn%2FRA4FGuQ%3D%3D"
    parameters += "&sigunguCd=" + str(11530)
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

bjdongCd = [10200,10300,10600,10700,10800,10900,11000,11100,11200]

for i in bjdongCd:
    bjdongCd = i
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
                            mainPurpsCdNm = node.find("mainPurpsCdNm").text
                            stcnsSchedDay = float(node.find("stcnsSchedDay").text)
                            realStcnsDay = float(node.find("realStcnsDay").text)
                            jiyukCdNm = node.find("jiyukCdNm").text
                            onedict = {'대지위치':platPlc, \
                                    '주용도코드명':mainPurpsCdNm, '착공예정일':stcnsSchedDay, \
                                    '실제착공일':realStcnsDay, \
                                    '지역코드명':jiyukCdNm}
                            dataList.append(onedict)

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

savedFilename = 'newGuro'+str(bjdongCd)+'.csv'

myframe = pd.DataFrame(dataList)
myframe.to_csv(savedFilename)

        
