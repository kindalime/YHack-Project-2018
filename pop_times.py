import populartimes
import math
import googlemaps
import datetime
from pathlib import Path
import os

API_KEY = "AIzaSyAklsbRetOAIkbuT97TP3gkHxCGobV8ZP4"
gmaps = googlemaps.Client(key=API_KEY)


def popular_times(location):
    coordinates = bound_coordinates(location, 0)
    extra_distance = 0.5
    results = populartimes.get(API_KEY, ["restaurant", "bakery", "bar", "cafe", "meal-delivery", "meal_takeaway"],
                               coordinates[0], coordinates[1])
    while (len(results) < 0):
        coordinates = bound_coordinates(location, extra_distance)
        results = populartimes.get(API_KEY, ["restaurant", "bakery", "bar", "cafe", "meal-delivery", "meal_takeaway"],
                                   coordinates[0], coordinates[1])
        extra_distance += 0.02
    return results

def bound_coordinates(location, additional_distance):
    if locality_type(location) == 'urban':
        distance = 0.03 + additional_distance
    elif locality_type(location) == 'suburban':
        distance = 0.09 + additional_distance
    elif locality_type(location == 'rural'):
        distance = 0.12 + additional_distance

    del_long = (distance * math.sqrt(2)) / (69 * math.cos(math.radians(location[0])))
    del_lat = (distance * math.sqrt(2)) / 69
    return (location[0] + del_lat, location[1] + del_long), (location[0] - del_lat, location[1] - del_long)

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

def append_new_info(location, results):
    origin = [location]
    destinations = []

    for i in range(len(results)):
        destinations.append(results[i].get('coordinates'))

    matrix = gmaps.distance_matrix(origin, destinations, units='imperial')

    now = datetime.datetime.now()
    day = now.weekday()
    hour = now.hour

    for i in range (len(results)):
        file = Path("/static/img/Company Images/" + results[i].get('name').replace(" ", "") + ".png/")
        if file.is_file():
            results[i].update({'file_exists?': 'true'})
        else:
            results[i].update({'file_exists?': 'false'})

        rating = results[i].get('rating')
        if rating >= 0 and rating < 0.5:
            stars = 'star0.png'
        elif rating >= 0.5 and rating < 1.5:
            stars = 'star1.png'
        elif rating >= 1.5 and rating < 2.5:
            stars = 'star2.png'
        elif rating >= 2.5 and rating < 3.5:
            stars = 'star3.png'
        elif rating >= 3.5 and rating < 4.5:
            stars = 'star4.png'
        else:
            stars = 'star5.png'
        
        distance = matrix.get('rows')[0].get('elements')[i].get('distance').get('text')
        
        results[i].update({'route_distance': distance})
        results[i].update({'stars': stars})
        data = results[i].get('populartimes')[day].get('data')
        bars = 'bar' + str(data[hour] // 10) + '.png'
        results[i].update({'bars': bars})

    return results

def main():
    location = (40.714120, -73.997269)
    print(append_new_info(location, popular_times(location)))
main()