import requests
from parsers import config

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
        print(r.json()['Result'])
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


cp = URA().getCarparks()
import datetime
import time
gmt_time = time.gmtime()

print(gmt_time)
gmt_time_to_dt = datetime.datetime.fromtimestamp(time.mktime(gmt_time))

gmt_plus = gmt_time_to_dt + datetime.timedelta(minutes = 480)
print(gmt_plus.time())

weekday = gmt_plus.date().weekday() < 5
print(weekday)

avails = URA().getAvail(
)
print(avails)

from SVYconverter import SVY21

for i in range(len(avails)):
    temp = avails[i]
    tempCoor = temp['geometries']
    newCoor = []
    for j in tempCoor:
        tempLatLon = [float(k) for k in j['coordinates'].split(',')]
        print(tempLatLon)
        convert = SVY21().computeLatLon(tempLatLon[0],tempLatLon[1])
        print(convert)
        newCoor.append({'coordinates':'%s,%s'%(convert[0],convert[1])})
    print(newCoor)
    avails[i]['geometries'] = newCoor

print(avails)

