import requests
from parsers import config
import datetime
import time
import re
from dateutil import tz
from SVYconverter import SVY21
import random
import json
import http.client


class URA:
    def __init__(self, getType = None):
        self.accessKey = config().getData('URA','accesskey')
        self.token = config().getData('URA','accesstoken')
        self.subject = getType
        self.conn = http.client.HTTPSConnection("www.ura.gov.sg")

    def makeRequest(self, getSet, url, payload, headers):
        self.conn.request(getSet, url, payload, headers)
        res = self.conn.getresponse()
        data = res.read().decode('utf8')
        dataJson = json.loads(data)
        return dataJson
    
    def getToken(self):
        payload = ''
        headers = {
        'AccessKey': self.accessKey
        }
        result = self.makeRequest("GET", "/uraDataService/insertNewToken.action", payload, headers)
        config().throwData('URA','AccessToken',result['Result'])
    
    def getCarparks(self):
        print(self.accessKey,self.token)
        payload = ''
        headers = {
            'AccessKey': self.accessKey,
            'User-Agent': 'curl/7.37.1',
            'Token': self.token
        }
        try:
            result = self.makeRequest("GET", "/uraDataService/invokeUraDS?service=Car_Park_Details", payload, headers)['Result']
        except:
            result = json.loads(config().getData('URA','carparks'))
        return result
    
    def getAvail(self):
        payload = ''
        headers = {
            'AccessKey': self.accessKey,
            'User-Agent': 'curl/7.37.1',
            'Token': self.token
        }
        try:
            result = self.makeRequest("GET", "/uraDataService/invokeUraDS?service=Car_Park_Availability", payload, headers)['Result']
        except:
            result = json.loads(config().getData('URA','avail'))
        return result

    def datingCP(self,cp = None):
        now = datetime.datetime.now()

        # Hardcode zones:
        from_zone = tz.tzutc()
        to_zone = tz.gettz('Asia/Singapore')

        utc = now

        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        timeInSg = utc.astimezone(to_zone)

        dayOfWeek = timeInSg.date().weekday()
    
        newCP = []
        for i in cp:
            temp = i
            rate = 0
            min = ''
            if dayOfWeek < 5:
                rate = i['weekdayRate']
                min = i['weekdayMin']
                del temp['weekdayRate']
                del temp['weekdayMin']
                del temp['satdayMin']
                del temp['satdayRate']
                del temp['sunPHMin']
                del temp['sunPHRate']
            elif dayOfWeek == 6:
                rate = i['sunPHMin']
                min = i['sunPHRate']
                del temp['weekdayRate']
                del temp['weekdayMin']
                del temp['satdayMin']
                del temp['satdayRate']
                del temp['sunPHMin']
                del temp['sunPHRate']
            else:
                rate = i['satdayRate']
                min = i['satdayMin']
                del temp['weekdayRate']
                del temp['weekdayMin']
                del temp['satdayMin']
                del temp['satdayRate']
                del temp['sunPHMin']
                del temp['sunPHRate']

            temp['rate'] = rate
            temp['min'] = min
            newCP.append(temp)

        return newCP
            

            


        
    def defCPAftTiming(self, cp):
        # print('into timing')
        gmt_time = time.gmtime()

        # print(gmt_time)
        gmt_time_to_dt = datetime.datetime.fromtimestamp(time.mktime(gmt_time))

        gmt_plus = gmt_time_to_dt + datetime.timedelta(minutes = 480)
        # print(gmt_plus.time())

        result = []

        for i in cp:
            if i['startTime'] <= gmt_plus.time() <= i['endTime'] or i['endTime'] < i['startTime'] and (i['startTime']<gmt_plus.time() or i['endTime'] > gmt_plus.time()):
                
                result.append(i)

        return result
    
    def defCPFormatted(self,cp): ## change rates to float, time to 24hr
        # print('into formatting')
        newCP = []
        count = 0
        for i in cp:
            if i['vehCat'] == 'Car':
                newCP.append(i)

                wdRate = i['weekdayRate']
                sunPHRate = i['sunPHRate']
                satdayRate = i['satdayRate']
                newWDRate = float(wdRate[1:])
                newSunPHRate = float(sunPHRate[1:])
                newSatDayRate = float(satdayRate[1:])
                
                newCP[count]['weekdayRate'] = newWDRate
                newCP[count]['sunPHRate'] = newSunPHRate
                newCP[count]['satdayRate'] = newSatDayRate

                startWS = re.search('\s',i['startTime']).span()
                startTime = '%s.00 %s'%(i['startTime'][:startWS[0]] , i['startTime'][startWS[1]:])
                convertedStart = datetime.datetime.strptime(startTime, '%I.%M.%S %p').time()

                endWS = re.search('\s',i['endTime']).span()
                endTime = '%s.00 %s'%(i['endTime'][:endWS[0]] , i['endTime'][endWS[1]:])
                convertedEnd = datetime.datetime.strptime(endTime, '%I.%M.%S %p').time()

                newCP[count]['startTime'] = convertedStart
                newCP[count]['endTime'] = convertedEnd
                newCP[count]['altRate'] = []

                count += 1

        return newCP

    def handleExtraRates(self,cp):
        seen = ''
        newCP = []
        count = -1
        # toggle = True
        for i in cp:
            if i['ppCode'] == seen:
                newCP[count]['altRate'].append({'rate' : i['rate'], 'min' : i['min']})
                # toggle = True
            else:
                count += 1
                newCP.append(i)
                seen = i['ppCode']

        return newCP
    
    def getCPFinal(self):
        # print('test 1')
        cp = self.getCarparks()
        # print('test2')
        newCP = self.defCPAftTiming((self.defCPFormatted(cp)))
        return self.convertToLatLon(newCP)

    def convertToLatLon(self,cp):
        for i in range(len(cp)):
            temp = cp[i]
            tempCoor = temp['geometries']
            newCoor = []
            for j in tempCoor:
                tempLatLon = [float(k) for k in j['coordinates'].split(',')]
                # print(tempLatLon)
                convert = SVY21().computeLatLon(tempLatLon[0],tempLatLon[1])
                # print(convert)
                newCoor.append({'coordinates':'%s,%s'%(convert[0],convert[1])})
            # print(newCoor)
            cp[i]['geometries'] = newCoor

        return cp

    def getAvailFinal(self):
        cp = self.getAvail()
        return self.convertToLatLon(cp)


# print(URA().getCarparks())
# import requests

# url = "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details"

# payload = ""
# headers = {
#   'AccessKey': 'fbc23f75-0023-47f7-a2e7-c22f489cdc75',
#   'Token': 'sFRZN2403V22PBswT2x7Kf4gbX0ke5ac2D554cM2Qc4Qf7t-T2ckJqd2W-9Mfy0e2y7cYH7Z2c5M0Sj5RX49aDJcjk3Td7Fx4-RQ'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

