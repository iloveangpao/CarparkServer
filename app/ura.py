import requests
from parsers import config
import os
import configparser
import json

class URA:
    def __init__(self, getType):
        # self.getData()
        self.accessKey = config().getData('URA','AccessKey')
        self.token = self.getToken()
        self.subject = getType
        # print('hello')

    def getToken(self):
        headers = {
            'AccessKey': self.accessKey,
            'User-Agent': 'curl/7.37.1'
        }
        
        r = requests.get("https://www.ura.gov.sg/uraDataService/insertNewToken.action",
                         headers=headers, data={}
                         )
        # print(r.json())
        print(r.json()['Result'])
        # print(self.__class__.__name__)
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
        # print(r.json()['Result'])
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
        # print(r.json()['Result'])
        return r.json()['Result']






ura = URA(1)
ura.getCarparks()


