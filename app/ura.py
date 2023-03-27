import requests
from parsers import config
import datetime
import time
import re

class URA:
    def __init__(self, getType = None):
        self.accessKey = config().getData('URA','AccessKey')
        self.token = self.getToken()
        self.subject = getType

    def getToken(self):
        headers = {
            'AccessKey': self.accessKey,
            'User-Agent': 'curl/7.37.1'
        }
        
        r = requests.get("https://www.ura.gov.sg/uraDataService/insertNewToken.action",
                         headers=headers, data={}
                         )
        print(r.json())
        result = r.json()['Result']
        # print(r.json()['Result'])
        config().throwData('URA','AccessToken',result)
        return r.json()['Result']
    
    def getCarparks(self):
        headers = {
            'AccessKey': self.accessKey,
            'User-Agent': 'curl/7.37.1',
            'Token': self.token
        }
        
        r = requests.get("https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details",
                         headers=headers, data={}
                         )
        return r.json()['Result']
    
    def getAvail(self):
        headers = {
            'AccessKey': self.accessKey,
            'User-Agent': 'curl/7.37.1',
            'Token': self.token
        }
        
        r = requests.get("https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Availability",
                         headers=headers, data={}
                         )
        return r.json()['Result']

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

            count += 1

        return newCP


    def getCPFinal(self):
        # print('test 1')
        cp = self.getCarparks()
        # print('test2')
        newCP = self.defCPAftTiming((self.defCPFormatted(cp)))
        return newCP

# print(URA().getCPFinal())
# cp = URA().getCarparks()
# import datetime
# import time
# import re
# gmt_time = time.gmtime()

# print(gmt_time)
# gmt_time_to_dt = datetime.datetime.fromtimestamp(time.mktime(gmt_time))

# gmt_plus = gmt_time_to_dt + datetime.timedelta(minutes = 480)
# print(gmt_plus.time())

# result = []

# for i in cp:
#     startWS = re.search('\s',i['startTime']).span()
#     startTime = '%s.00 %s'%(i['startTime'][:startWS[0]] , i['startTime'][startWS[1]:])
#     convertedStart = datetime.datetime.strptime(startTime, '%I.%M.%S %p').time()

#     endWS = re.search('\s',i['endTime']).span()
#     endTime = startTime = '%s.00 %s'%(i['endTime'][:startWS[0]] , i['endTime'][startWS[1]:])
#     convertedEnd = datetime.datetime.strptime(endTime, '%I.%M.%S %p').time()
#     print(convertedStart,convertedEnd)

#     if convertedStart <= gmt_plus.time() <= convertedEnd or convertedEnd < convertedStart and (convertedStart<gmt_plus.time() or convertedEnd > gmt_plus.time()):
#         result.append(i)

# print(result)


# weekday = gmt_plus.date().weekday() < 5
# print(weekday)



