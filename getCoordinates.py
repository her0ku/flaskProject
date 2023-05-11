from geopy.geocoders import Nominatim


def get_location(address):
    geolocator = Nominatim(user_agent="my-awesome-project")
    location = geolocator.geocode(address)
    location = (location.longitude, location.latitude)
    return location


def get_coordinates(address):
    print(address)
    geolocator = Nominatim(user_agent="my-awesome-project")
    location = geolocator.geocode(address)
    return location.longitude, location.latitude