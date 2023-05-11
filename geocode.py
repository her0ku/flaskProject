from geopy.geocoders import Nominatim

address = "Ногинск, улица Советской Конституции, 29 "

geolocator = Nominatim(user_agent="my-awesome-project")
location = geolocator.geocode(address)

if location is None:
    print("Координаты не найдены")
else:
    print("Широта:", location.latitude)
    print("Долгота:", location.longitude)
