import populartimes
import math
import googlemaps

API_KEY = "AIzaSyCXkN4IwdOUzq8JDaBMdR4OK5JUaSmACJ4"
gmaps = googlemaps.Client(key=API_KEY)

def popular_times(p1, p2):
    return populartimes.get(API_KEY, ["restaurant"], p1, p2)

def bound_coordinates(location):
    if locality_type(location) == 'urban':
        distance = 2.5
    elif locality_type(location) == 'suburban':
        distance = 0.5
    elif locality_type(location == 'rural'):
        distance = 5

    del_long = (distance * math.sqrt(2)) / (69 * math.cos(math.radians(location[0])))
    del_lat = (distance * math.sqrt(2)) / 69
    return (location[0] - del_lat, location[1] + del_long), (location[0] + del_lat, location[1] - del_long)

def locality_type(location):
    reverse_geocode_result = gmaps.reverse_geocode(location)
    address_comp = reverse_geocode_result[0].get('address_components')

    for i in range(len(address_comp)):
        if len(address_comp) - i - 1 == 0:
            return 'out-of-bounds'
        else:
            if 'locality' in address_comp[len(address_comp) - i - 1].get('types') or 'administrative-area-level-3' in address_comp[len(address_comp) - i - 1].get('types'):
                return'urban'
            elif any('sublocality' in s for s in address_comp[len(address_comp) - i - 1].get('types')):
                return'suburban'
            elif 'neighborhood' in address_comp[len(address_comp) - i - 1].get('types'):
                return 'rural'


def main():
    print(locality_type((35.1495, 90.0490)))
    coordinates = bound_coordinates((35.1495, 90.0490))
    print(coordinates)
    list = popular_times((35.09826037817489, 90.11166673537485), (35.200739621825115, 89.98633326462516))
    print(list)
    print(len(list))


main()
