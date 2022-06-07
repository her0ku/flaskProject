from dadata import Dadata
token = "87da735bfc5c412b4d618f9ce17296aea09f505d"
secret = "8388738cb9f3b8fd029f7fe446c36e2cf81d8fd9"


def get_location(address):
    location = tuple()
    dadata = Dadata(token, secret)
    result = dadata.clean("address", address)
    location = (result['geo_lon'], result['geo_lat'])
    return location


def get_coordinates(address):
    print(address)
    dadata = Dadata(token, secret)
    result = dadata.clean('address', address)
    return result['geo_lon'], result['geo_lat']