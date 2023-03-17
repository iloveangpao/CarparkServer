
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
import sys
sys.path.append(os.getcwd())
print(os.getcwd())
from app import ura
from ura import URA

def create_carpark():
    print('working')
    ura = URA()
    cp = ura.getCarparks()
    # for i in cp:
    #     if len(i['geometries']) > 1:
    #         print(i)
    #         print(type(i['geometries']))
    #         print(i['geometries'])

    temp = cp[0]
    print(temp)
    print(type(temp['geometries']))
    print(temp['geometries'])
    num = len(temp['geometries'])
    print(num)

    locations = []
    for loc in temp['geometries']:
        print(loc)
        coordinates = loc['coordinates']
        locations.append(tuple(loc['coordinates'].split(',')))
    print(locations)
    


create_carpark()