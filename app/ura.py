import requests
from app.parsers import config
import os
import configparser
import json

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
