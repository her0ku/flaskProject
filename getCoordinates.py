from geopy.geocoders import Nominatim


def get_address_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="my-awesome-project") # Указываем ваше приложение (может быть любое имя)
    location = geolocator.reverse((latitude, longitude), language='ru') # language='ru' указывает, что результат будет на русском языке

    if location:
        address = location.address
        return address
    else:
        return "Адрес не найден"

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