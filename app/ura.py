import requests
import os
import configparser
import json

class URA:
    def __init__(self, getType):
        self.getData()
        self.token = self.getToken()
        self.subject = getType
        print('hello')

    def getToken(self):
        r = requests.get(self.tokenURL, 
        headers={'AccessKey':self.accessKey},allow_redirects=False)
        print(r.status_code,r.json())

    def getData(self):
        Config = configparser.ConfigParser()
        Config.read('./app/config.ini')
        self.accessKey = Config.get('URA',  'AccessKey')
        
        self.tokenURL = Config.get('URA', 'TokenURL')
        print(self.accessKey,self.tokenURL)


ura = URA(1)
ura.getToken()


