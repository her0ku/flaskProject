from dadata import Dadata
token = "2ddf86daf87c4b6cbd59baa17576f2a8e9b48c88"
secret = "60c33b86efbfbc63274f0bbbb5883d4cc6251e29"


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