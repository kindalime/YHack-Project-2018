import populartimes
import math
import googlemaps

API_KEY = "AIzaSyCXkN4IwdOUzq8JDaBMdR4OK5JUaSmACJ4"
gmaps = googlemaps.Client(key=API_KEY)

def popular_times(location):
    coordinates = bound_coordinates(location, 0)
    extra_distance = 0.5
    results = populartimes.get(API_KEY, ["restaurant", "bakery", "bar", "cafe", "meal-delivery", "meal_takeaway"],
                               coordinates[0], coordinates[1])
    while (len(results) < 30):
        coordinates = bound_coordinates(location, extra_distance)
        results = populartimes.get(API_KEY, ["restaurant", "bakery", "bar", "cafe", "meal-delivery", "meal_takeaway"],
                                   coordinates[0], coordinates[1])
        extra_distance += 0.5
    return results

def bound_coordinates(location, additional_distance):
    if locality_type(location) == 'urban':
        distance = 0.1 + additional_distance
    elif locality_type(location) == 'suburban':
        distance = 0.5 + additional_distance
    elif locality_type(location == 'rural'):
        distance = 1 + additional_distance

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

