import requests
from SVYconverter import SVY21

class OneMap:
    def __init__(self) -> None:
        self.token = self.getToken()
        pass

    def getToken(self):
        body = {
            "email" : "YLIM171@e.ntu.edu.sg",
            "password" : "WErock123!!!!"
        }

        r = requests.post("https://developers.onemap.sg/privateapi/auth/post/getToken", 
                          json = body)

        
        return r.json()['access_token']


    def getSearch(self, searchVal : str):
        params = {
            'searchVal': searchVal,
            'returnGeom': 'Y',
            'getAddrDetails' : 'Y',
            'pageNum': 1
        }
        
        r = requests.get("https://developers.onemap.sg/commonapi/search",
                         params=params, data={}
                         )
        # print(r.json())
        result = r.json()['results']
        return result
    
    def getRoute(self, start: list, end: list, SVY: bool = True):
        actStart = ','.join( [str(comp) for comp in start] )
        actEnd = ','.join( [str(comp) for comp in end] )
        if SVY:
            actStart = ','.join( [str(comp) for comp in SVY21().computeLatLon(float(start[0]),float(start[1]))] )
            actEnd = ','.join( [str(comp) for comp in SVY21().computeLatLon(float(end[0]),float(end[1]))] )


        params = {
            'start': actStart,
            'end': actEnd,
            'routeType' : 'drive',
            'token': self.token
        }

        headers = {
            'User-Agent': 'curl/7.37.1',
            'AccessKey': 'fbc23f75-0023-47f7-a2e7-c22f489cdc75'
        }
        
        r = requests.get("https://developers.onemap.sg/privateapi/routingsvc/route",
                         params=params, headers=headers
                         )
        # print(r.json())

        result = r.json()
        if 'error' in result:
            raise Exception(result['error'])
        return result['route_summary']

    



print(OneMap().getRoute([1.31972,103.8421],[1.319728905,103.8421581],False))