from onemap import OneMap
import copy
from geopy.distance import geodesic as GD
from SVYconverter import SVY21
from db.schemas.carparkSchema import *

class Filter():
    def __init__(self) -> None:

        pass

    def sort(self, toSort: str, data: list[Carpark], reverse: bool):
        result = []

        size = len(data)

        for i in data:
            temp = dict(i)
            if temp[toSort] == None:
                temp['toSort'] = -1
            else:
                temp['toSort'] = temp[toSort]
            result.append(temp)
        
        self.quickSort(result, 0, size - 1)
        if reverse:
            result.reverse()
        print(result)
        return result

    def getNearby(self, data: list[Carpark], base: list):
        QUOTA = 1.0
        withinFiveMin = []
        convBase = SVY21().computeLatLon(float(base[0]),float(base[1]))
        for i in data:
            temp = dict(i)
            # timeTaken = QUOTA + 1
            tempXY = [float(coor) for coor in dict(temp['locations'])['locations'][0]]
            
            try:
                # timeTaken = OneMap().getRoute(tempXY,base)['total_time']
                # print(timeTaken)
                # i['total_time'] = timeTaken/60
                print(GD(convBase,tempXY))
                if GD(convBase,tempXY) <=  QUOTA:
                    withinFiveMin.append(i)
            except Exception as e:
                print(e)
            

        return withinFiveMin



    def quickSort(self, array, low, high):
        if low < high:
    
            # Find pivot element such that
            # element smaller than pivot are on the left
            # element greater than pivot are on the right
            pi = self.partition(array, low, high)
    
            # Recursive call on the left of pivot
            self.quickSort(array, low, pi - 1)
    
            # Recursive call on the right of pivot
            self.quickSort(array, pi + 1, high)

    def partition(self, array,low,high):
            # choose the rightmost element as pivot
        pivot = array[high]['toSort']
    
        # pointer for greater element
        i = low - 1
    
        # traverse through all elements
        # compare each element with pivot
        for j in range(low, high):
            if array[j]['toSort'] <= pivot:
    
                # If element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1
    
                # Swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])
    
        # Swap the pivot element with the greater element specified by i
        (array[i + 1], array[high]) = (array[high], array[i + 1])
    
        # Return the position from where partition is done
        return i + 1




