import requests
import os
import configparser
import json

class URA:
    def __init__(self, getType):
        # self.getData()
        self.token = self.getToken()
        self.subject = getType
        print('hello')

    def getToken(self):
        # print(f"using access token: {self.accessKey}")
        # r = requests.get(self.tokenURL, 
        # headers={'AccessKey':self.accessKey})
        headers = {
            'AccessKey': 'fbc23f75-0023-47f7-a2e7-c22f489cdc75',
            'User-Agent': 'curl/7.37.1'
        }
        
        r = requests.get("https://www.ura.gov.sg/uraDataService/insertNewToken.action",
                         headers=headers, data={}
                         )
        print(r.status_code)
        print(r.text)
        print(r.json())

    def getData(self):
        Config = configparser.ConfigParser()
        Config.read('./app/config.ini')
        self.accessKey = Config.get('URA',  'AccessKey')
        
        self.tokenURL = Config.get('URA', 'TokenURL')
        print(self.accessKey,self.tokenURL)


ura = URA(1)
ura.getToken()


